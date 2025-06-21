"""Web 라우트 최소 테스트 (FastAPI TestClient)."""
from __future__ import annotations

import uuid

from fastapi.testclient import TestClient

from nojam.main import app

client = TestClient(app)


def _dummy_answers() -> dict[str, str]:
    return {f"q{i}": "A" for i in range(1, 11)}


def test_full_flow() -> None:
    # GET /quiz
    res = client.get("/quiz")
    assert res.status_code == 200
    assert "<form" in res.text

    # POST /submit
    res = client.post("/submit", data=_dummy_answers(), follow_redirects=False)
    assert res.status_code == 302
    location = res.headers["location"]
    assert location.startswith("/result/")

    # GET /result/{id}
    res = client.get(location)
    assert res.status_code == 200
    assert "당신의 결과는" in res.text
