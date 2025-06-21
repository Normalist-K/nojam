"""SQLite 기반 Answer 저장소.

비동기 aiosqlite를 사용하여 CRUD를 제공한다.
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Sequence

import aiosqlite

RESULT_TYPES = {"7080", "IMF", "ACT", "DRM", "PHONE", "ANA", "TREND", "JUNK"}


class AnswerRepository:
    """answers 테이블에 대한 비동기 CRUD."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._conn: aiosqlite.Connection | None = None

    async def _get_conn(self) -> aiosqlite.Connection:
        """싱글턴 커넥션 반환."""
        if self._conn is None:
            self._conn = await aiosqlite.connect(self._db_path, uri=self._db_path.startswith("file:"))
            self._conn.row_factory = aiosqlite.Row
        return self._conn

    async def init(self) -> None:
        """answers 테이블이 없으면 생성한다."""
        conn = await self._get_conn()
        await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS answers (
                    id TEXT PRIMARY KEY,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    answers_json TEXT NOT NULL,
                    result_type TEXT CHECK(result_type IN ('7080','IMF','ACT','DRM','PHONE','ANA','TREND','JUNK')),
                    ua_hash CHAR(64)
                );
                """
        )
        await conn.commit()

    async def add(
        self,
        *,
        id: str,
        answers_json: str | dict[str, Any],
        result_type: str,
        ua_hash: str,
    ) -> None:
        """레코드 삽입."""
        if result_type not in RESULT_TYPES:
            raise ValueError("Invalid result_type")
        if isinstance(answers_json, dict):
            answers_json = json.dumps(answers_json, ensure_ascii=False)
        conn = await self._get_conn()
        await conn.execute(
            """
            INSERT INTO answers (id, answers_json, result_type, ua_hash)
            VALUES (?, ?, ?, ?)
            """,
            (id, answers_json, result_type, ua_hash),
        )
        await conn.commit()

    async def get(self, id: str) -> dict[str, Any] | None:
        """id로 단일 조회."""
        conn = await self._get_conn()
        async with conn.execute("SELECT * FROM answers WHERE id = ?", (id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None

    async def list(self) -> Sequence[dict[str, Any]]:
        """전체 조회 (최근 생성 순)."""
        conn = await self._get_conn()
        async with conn.execute(
            "SELECT * FROM answers ORDER BY datetime(created_at) DESC"
        ) as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]

    async def delete(self, id: str) -> None:
        """id로 삭제."""
        conn = await self._get_conn()
        await conn.execute("DELETE FROM answers WHERE id = ?", (id,))
        await conn.commit()
