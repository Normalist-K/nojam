"""퀴즈 결과 계산 로직.

JSON 기반 플랫폼으로 마이그레이션된 퀴즈 서비스.
기존 하드코딩된 매핑은 하위 호환성을 위해 유지하되,
새로운 JSON 기반 시스템을 우선적으로 사용한다.
"""

from __future__ import annotations

import logging
from collections import Counter
from typing import Dict, Mapping, Optional

from .loader import get_quiz_loader
from .scoring import ScoringEngine

logger = logging.getLogger(__name__)

# 기존 하드코딩된 매핑 (하위 호환성용)
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


def calculate_result_type(
    answers: Mapping[str, str], quiz_id: Optional[str] = None
) -> str:
    """사용자 선택지를 받아 최다 득점 결과 코드를 반환.

    JSON 기반 시스템을 우선적으로 사용하고, 실패시 기존 하드코딩된 로직으로 폴백한다.

    매개변수
    --------
    answers : Mapping[str, str]
        예: {"q1": "C", "q2": "A", ...} (기존 형식)
        또는 {"q1": "q1_c", "q2": "q2_a", ...} (새 형식)
    quiz_id : Optional[str]
        사용할 퀴즈 ID. None이면 기본 퀴즈 또는 하드코딩된 로직 사용

    반환
    -----
    str
        최종 결과 코드(8가지 중 하나)
    """
    # JSON 기반 시스템 시도
    if quiz_id is not None:
        try:
            return calculate_result_with_json(answers, quiz_id)
        except Exception as e:
            logger.warning(f"JSON 기반 계산 실패, 기존 로직으로 폴백: {e}")

    # 기본 퀴즈 시도 (mind-age-test)
    try:
        return calculate_result_with_json(answers, "mind-age-test")
    except Exception as e:
        logger.warning(f"기본 JSON 퀴즈 계산 실패, 하드코딩 로직으로 폴백: {e}")

    # 기존 하드코딩된 로직으로 폴백
    return _calculate_legacy_result(answers)


def calculate_result_with_json(answers: Mapping[str, str], quiz_id: str) -> str:
    """JSON 기반 퀴즈로 결과를 계산한다.

    매개변수
    --------
    answers : Mapping[str, str]
        문항 ID -> 선택지 매핑
        기존 형식 {"q1": "A"} 또는 새 형식 {"q1": "q1_a"} 모두 지원
    quiz_id : str
        사용할 퀴즈 ID

    반환
    -----
    str
        결과 유형 코드
    """
    loader = get_quiz_loader()
    quiz = loader.load_quiz(quiz_id)

    # 답변 형식 변환 (기존 A/B/C/D -> 새 q1_a/q1_b/q1_c/q1_d)
    normalized_answers = _normalize_answers(answers, quiz)

    # 점수 계산
    scoring_engine = ScoringEngine(quiz)
    return scoring_engine.calculate_result(normalized_answers)


def get_score_breakdown(
    answers: Mapping[str, str], quiz_id: Optional[str] = None
) -> Dict[str, int]:
    """결과 유형별 점수 분포를 반환한다.

    매개변수
    --------
    answers : Mapping[str, str]
        문항 ID -> 선택지 매핑
    quiz_id : Optional[str]
        사용할 퀴즈 ID

    반환
    -----
    Dict[str, int]
        결과 유형별 점수 딕셔너리
    """
    # JSON 기반 시스템 시도
    if quiz_id is not None:
        try:
            loader = get_quiz_loader()
            quiz = loader.load_quiz(quiz_id)
            normalized_answers = _normalize_answers(answers, quiz)
            scoring_engine = ScoringEngine(quiz)
            return scoring_engine.get_score_breakdown(normalized_answers)
        except Exception as e:
            logger.warning(f"JSON 기반 점수 분포 계산 실패: {e}")

    # 기본 퀴즈 시도
    try:
        loader = get_quiz_loader()
        quiz = loader.load_quiz("mind-age-test")
        normalized_answers = _normalize_answers(answers, quiz)
        scoring_engine = ScoringEngine(quiz)
        return scoring_engine.get_score_breakdown(normalized_answers)
    except Exception as e:
        logger.warning(f"기본 JSON 퀴즈 점수 분포 계산 실패: {e}")

    # 기존 하드코딩된 로직으로 폴백
    return _calculate_legacy_breakdown(answers)


def _normalize_answers(answers: Mapping[str, str], quiz) -> Dict[str, str]:
    """답변 형식을 새로운 형식으로 정규화한다.

    기존: {"q1": "A", "q2": "B"}
    새로운: {"q1": "q1_a", "q2": "q2_b"}
    """
    normalized = {}

    for question in quiz.questions:
        qid = question.id
        if qid not in answers:
            continue

        answer = answers[qid]

        # 이미 새 형식인지 확인
        if answer.startswith(f"{qid}_"):
            normalized[qid] = answer
        else:
            # 기존 형식(A/B/C/D)을 새 형식으로 변환
            choice_letter = answer.upper()
            choice_id = f"{qid}_{choice_letter.lower()}"

            # 해당 선택지가 실제로 존재하는지 확인
            valid_choice = False
            for choice in question.choices:
                if choice.id == choice_id:
                    valid_choice = True
                    break

            if valid_choice:
                normalized[qid] = choice_id
            else:
                raise ValueError(
                    f"문항 {qid}에서 선택지 {choice_letter}({choice_id})를 찾을 수 없습니다."
                )

    return normalized


def _calculate_legacy_result(answers: Mapping[str, str]) -> str:
    """기존 하드코딩된 로직으로 결과를 계산한다."""
    if len(answers) != 10:
        raise ValueError("10문항 답변이 모두 필요합니다.")

    counter: Counter[str] = Counter()

    for qid, choice in answers.items():
        try:
            result_type = QUIZ_MAPPING[qid][choice]
        except KeyError as exc:
            raise ValueError(f"잘못된 질문/선택지: {qid} {choice}") from exc
        counter[result_type] += 1

    # 최다 득점 구하기
    max_score = max(counter.values())
    winners = [t for t, score in counter.items() if score == max_score]

    # 동점 시 알파벳순으로 결정
    winners.sort()
    return winners[0]


def _calculate_legacy_breakdown(answers: Mapping[str, str]) -> Dict[str, int]:
    """기존 하드코딩된 로직으로 점수 분포를 계산한다."""
    counter: Counter[str] = Counter()

    for qid, choice in answers.items():
        if qid in QUIZ_MAPPING and choice in QUIZ_MAPPING[qid]:
            result_type = QUIZ_MAPPING[qid][choice]
            counter[result_type] += 1

    # 모든 결과 유형을 포함하여 반환
    result = {}
    for result_type in RESULT_TYPES:
        result[result_type] = counter.get(result_type, 0)

    return result
