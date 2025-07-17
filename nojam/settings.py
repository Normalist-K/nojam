"""프로젝트 공통 설정 (로깅 등)."""

from __future__ import annotations

import logging
import os
import sys
from typing import Any

import structlog


def configure_logging() -> None:
    """structlog JSON 로깅 기본 설정."""
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            timestamper,
            structlog.processors.add_log_level,
            structlog.processors.EventRenamer("message"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    )


# ------------------------------------------------------------
# 환경변수 설정
# ------------------------------------------------------------

# Kakao SDK 설정
KAKAO_JAVASCRIPT_KEY = os.getenv("KAKAO_JAVASCRIPT_KEY", "")
KAKAO_JAVASCRIPT_KEY_DEV = "your-dev-key-here"  # 개발용 테스트 키


def get_kakao_javascript_key() -> str:
    """환경에 따른 Kakao JavaScript Key 반환."""
    if KAKAO_JAVASCRIPT_KEY:
        return KAKAO_JAVASCRIPT_KEY
    # 개발 환경에서는 개발용 키 사용 (실제로는 실제 키를 설정해야 함)
    return KAKAO_JAVASCRIPT_KEY_DEV


# ------------------------------------------------------------
# Analytics helper wrappers
# ------------------------------------------------------------


def log_ga4_event(event_name: str, params: dict[str, Any] | None = None) -> None:
    """GA4 이벤트 로깅 (Stub)."""
    structlog.get_logger("ga4").info(event_name, **(params or {}))


def log_ad_metric(
    metric: str, value: float | int, extra: dict[str, Any] | None = None
) -> None:
    """광고 수익·RPM·CTR 등 지표 로깅."""
    data = {"metric": metric, "value": value}
    if extra:
        data.update(extra)
    structlog.get_logger("ad").info("ad_metric", **data)
