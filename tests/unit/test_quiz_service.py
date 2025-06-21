"""calculate_result_type 단위 테스트."""
from __future__ import annotations

import pytest

from nojam.services.quiz import calculate_result_type


def _majority_7080_answers() -> dict[str, str]:
    """7080이 6점으로 1위인 답변 세트 반환."""
    return {
        "q1": "C",  # 7080
        "q2": "A",  # 7080
        "q3": "B",  # 7080
        "q4": "A",  # ANA
        "q5": "B",  # DRM
        "q6": "B",  # PHONE
        "q7": "C",  # 7080
        "q8": "A",  # 7080
        "q9": "A",  # 7080
        "q10": "B",  # DRM
    }


@pytest.mark.parametrize(
    "answers, expected",
    [(_majority_7080_answers(), "7080")],
)
def test_calculate_result_type(answers: dict[str, str], expected: str) -> None:
    assert calculate_result_type(answers) == expected
