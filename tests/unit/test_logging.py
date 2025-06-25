"""structlog 설정 & 헬퍼 함수 테스트."""
from __future__ import annotations

import json
from io import StringIO
from typing import Any

import structlog

import nojam.settings as settings


def _capture_log() -> tuple[StringIO, Any]:
    stream = StringIO()
    structlog.configure(
        processors=[
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.PrintLoggerFactory(file=stream),
    )
    return stream, structlog.get_logger()


def test_ga4_log_helper() -> None:
    stream, _ = _capture_log()
    settings.log_ga4_event("result_generated", {"type": "7080"})
    data: dict[str, Any] = json.loads(stream.getvalue())
    assert data["event"] == "result_generated"
    assert data["type"] == "7080"


def test_ad_metric_helper() -> None:
    stream, _ = _capture_log()
    settings.log_ad_metric("rpm", 2500)
    data = json.loads(stream.getvalue())
    assert data["metric"] == "rpm"
    assert data["value"] == 2500
