"""외부 SDK Stub 테스트."""
from __future__ import annotations

from nojam.external import kakao_stub, adsense_stub


def test_kakao_share_stub() -> None:
    resp = kakao_stub.share_link("테스트 제목", "https://example.com")
    assert resp["status"] == "success"
    history = kakao_stub.get_call_history()
    assert len(history) == 1
    func_name, payload = history[0]
    assert func_name == "share_link"
    assert payload["title"] == "테스트 제목"
    assert payload["url"] == "https://example.com"


def test_adsense_render_stub() -> None:
    resp = adsense_stub.render_ad("slot-123")
    assert resp["status"] == "rendered"
    history = adsense_stub.get_render_history()
    assert len(history) == 1
    assert history[0]["slot_id"] == "slot-123"
