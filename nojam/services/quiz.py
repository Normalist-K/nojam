"""퀴즈 결과 계산 로직.

`calculate_result_type` 는 10개 문항에 대한 사용자의 선택지를 받아
8가지 결과 코드 중 하나를 반환한다.
문항-선택지→결과 매핑은 고정 상수 `QUIZ_MAPPING`에 정의한다.
"""
from __future__ import annotations

from collections import Counter
from typing import Dict, Mapping

# 문항 ID("q1" … "q10") → 선택지(A/B/C/D) → 결과 코드
QUIZ_MAPPING: dict[str, dict[str, str]] = {
    "q1": {"A": "ANA", "B": "PHONE", "C": "7080", "D": "TREND"},
    "q2": {"A": "7080", "B": "DRM", "C": "JUNK", "D": "PHONE"},
    "q3": {"A": "PHONE", "B": "7080", "C": "ACT", "D": "TREND"},
    "q4": {"A": "ANA", "B": "DRM", "C": "PHONE", "D": "IMF"},
    "q5": {"A": "ACT", "B": "DRM", "C": "TREND", "D": "JUNK"},
    "q6": {"A": "IMF", "B": "PHONE", "C": "ANA", "D": "TREND"},
    "q7": {"A": "IMF", "B": "ACT", "C": "7080", "D": "DRM"},
    "q8": {"A": "7080", "B": "IMF", "C": "DRM", "D": "TREND"},
    "q9": {"A": "7080", "B": "ACT", "C": "DRM", "D": "PHONE"},
    "q10": {"A": "ANA", "B": "DRM", "C": "TREND", "D": "JUNK"},
}

RESULT_TYPES = {
    "7080",
    "IMF",
    "ACT",
    "DRM",
    "PHONE",
    "ANA",
    "TREND",
    "JUNK",
}


def calculate_result_type(answers: Mapping[str, str]) -> str:
    """사용자 선택지를 받아 최다 득점 결과 코드를 반환.

    매개변수
    --------
    answers : Mapping[str, str]
        예: {"q1": "C", "q2": "A", ...}

    반환
    -----
    str
        최종 결과 코드(8가지 중 하나)
    """
    if len(answers) != 10:
        raise ValueError("10문항 답변이 모두 필요합니다.")

    counter: Counter[str] = Counter()

    for qid, choice in answers.items():
        try:
            result_type = QUIZ_MAPPING[qid][choice]
        except KeyError as exc:  # invalid qid or choice
            raise ValueError(f"잘못된 질문/선택지: {qid} {choice}") from exc
        counter[result_type] += 1

    # 최다 득점 구하기
    max_score = max(counter.values())
    winners = [t for t, score in counter.items() if score == max_score]

    # 동점 시 알파벳순으로 결정 (안정적·예측 가능)
    winners.sort()
    return winners[0]
