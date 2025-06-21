"""AnswerRepository CRUD 단위 테스트."""

from __future__ import annotations

import hashlib
import json
import uuid

import pytest

from nojam.db.repository import AnswerRepository, RESULT_TYPES


@pytest.mark.asyncio
async def test_answer_crud() -> None:
    async with AnswerRepository() as repo:
        await repo.init()

        answer_id = str(uuid.uuid4())
        answers = {"q1": "A", "q2": "B"}
        result_type = next(iter(RESULT_TYPES))
        ua_hash = hashlib.sha256(b"dummy").hexdigest()

        # Create
        await repo.add(
            id=answer_id, answers_json=answers, result_type=result_type, ua_hash=ua_hash
        )

        # Read
        retrieved = await repo.get(answer_id)
        assert retrieved is not None
        assert retrieved["id"] == answer_id
        assert json.loads(retrieved["answers_json"]) == answers

        # List
        items = await repo.list()
        assert len(items) == 1

        # Delete
        await repo.delete(answer_id)
        assert await repo.get(answer_id) is None
