"""Kakao JavaScript SDK 호출을 대체하는 테스트용 Stub.

실제 Kakao SDK 대신 동일한 인터페이스를 흉내 내어, 호출 횟수·파라미터를 기록한다.
"""
from __future__ import annotations

from typing import List, Tuple

_CALL_HISTORY: List[Tuple[str, dict]] = []


def share_link(title: str, url: str) -> dict[str, str]:
    """카카오톡 공유 링크 Stub.

    실제 SDK는 비동기로 동작하지만, 단순화 위해 동기 함수로 구현한다.
    """
    payload = {"title": title, "url": url}
    _CALL_HISTORY.append(("share_link", payload))
    # 실제 SDK는 Promise 형태지만 Stub은 즉시 성공 응답 반환
    return {"status": "success", "data": payload}


def get_call_history() -> list[tuple[str, dict]]:
    """테스트용: 함수 호출 기록을 가져온 뒤 초기화."""
    history = _CALL_HISTORY.copy()
    _CALL_HISTORY.clear()
    return history
