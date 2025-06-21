"""Google AdSense JS SDK Stub.

광고 슬롯 렌더 여부를 테스트하기 위한 간단한 모킹 구현.
"""
from __future__ import annotations

from typing import List, Dict

_RENDERED_SLOTS: List[Dict[str, str]] = []


def render_ad(slot_id: str) -> dict[str, str]:
    """광고 슬롯을 렌더했다고 기록하고 가짜 응답 반환."""
    slot = {"slot_id": slot_id}
    _RENDERED_SLOTS.append(slot)
    return {"status": "rendered", **slot}


def get_render_history() -> list[dict[str, str]]:
    """테스트용: 렌더된 슬롯 기록을 가져온 뒤 초기화."""
    history = _RENDERED_SLOTS.copy()
    _RENDERED_SLOTS.clear()
    return history
