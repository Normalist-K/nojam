"""Scoring Engine for JSON-driven platform.

다양한 점수 계산 방식을 지원하는 범용 점수 계산 엔진.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping

from ..models.quiz import Quiz, ScoringMethod


class ScoringEngine:
    """JSON 기반 점수 계산 엔진."""

    def __init__(self, quiz: Quiz):
        """
        매개변수
        --------
        quiz : Quiz
            점수 계산에 사용할 퀴즈 정의
        """
        self.quiz = quiz
        self.scoring_method = quiz.config.scoring_method

    def calculate_result(self, answers: Mapping[str, str]) -> str:
        """사용자 답변을 받아 결과 유형을 계산한다.

        매개변수
        --------
        answers : Mapping[str, str]
            문항 ID -> 선택지 ID 매핑
            예: {"q1": "q1_c", "q2": "q2_a", ...}

        반환
        -----
        str
            최종 결과 유형 코드

        예외
        ----
        ValueError
            답변 수가 부족하거나 잘못된 문항/선택지인 경우
        """
        expected_count = self.quiz.config.question_count
        if len(answers) != expected_count:
            raise ValueError(
                f"{expected_count}문항 답변이 모두 필요합니다. (받은 답변: {len(answers)})"
            )

        # 점수 계산 방식에 따라 분기
        if self.scoring_method == ScoringMethod.SIMPLE_COUNT:
            return self._calculate_simple_count(answers)
        elif self.scoring_method == ScoringMethod.WEIGHTED_SUM:
            return self._calculate_weighted_sum(answers)
        elif self.scoring_method == ScoringMethod.PERCENTAGE:
            return self._calculate_percentage(answers)
        else:
            raise ValueError(f"지원하지 않는 점수 계산 방식: {self.scoring_method}")

    def _calculate_simple_count(self, answers: Mapping[str, str]) -> str:
        """Simple Count 방식으로 점수 계산.

        각 선택지는 특정 결과 유형에 1점을 추가한다.
        최다 득점 유형이 결과가 되며, 동점시 알파벳순으로 결정한다.
        """
        counter: Counter[str] = Counter()

        # 문항별로 선택지 찾기 및 점수 추가
        for question in self.quiz.questions:
            answer_choice_id = answers.get(question.id)
            if answer_choice_id is None:
                raise ValueError(f"문항 {question.id}에 대한 답변이 없습니다.")

            # 해당 문항에서 선택지 찾기
            selected_choice = None
            for choice in question.choices:
                if choice.id == answer_choice_id:
                    selected_choice = choice
                    break

            if selected_choice is None:
                raise ValueError(
                    f"문항 {question.id}에서 선택지 {answer_choice_id}를 찾을 수 없습니다."
                )

            # 결과 유형에 1점 추가
            counter[selected_choice.result_type] += 1

        # 최다 득점 결과 찾기
        if not counter:
            raise ValueError("점수 계산 결과가 없습니다.")

        max_score = max(counter.values())
        winners = [
            result_type for result_type, score in counter.items() if score == max_score
        ]

        # 동점 시 알파벳순으로 결정 (안정적·예측 가능)
        winners.sort()
        return winners[0]

    def _calculate_weighted_sum(self, answers: Mapping[str, str]) -> str:
        """Weighted Sum 방식으로 점수 계산 (향후 구현)."""
        # TODO: Phase 2에서 구현
        raise NotImplementedError("Weighted Sum 방식은 Phase 2에서 구현 예정입니다.")

    def _calculate_percentage(self, answers: Mapping[str, str]) -> str:
        """Percentage 방식으로 점수 계산 (향후 구현)."""
        # TODO: Phase 2에서 구현
        raise NotImplementedError("Percentage 방식은 Phase 2에서 구현 예정입니다.")

    def get_score_breakdown(self, answers: Mapping[str, str]) -> dict[str, int]:
        """결과 유형별 점수 분포를 반환한다.

        매개변수
        --------
        answers : Mapping[str, str]
            문항 ID -> 선택지 ID 매핑

        반환
        -----
        Dict[str, int]
            결과 유형별 점수 딕셔너리
        """
        if self.scoring_method != ScoringMethod.SIMPLE_COUNT:
            raise NotImplementedError(
                "점수 분포는 현재 Simple Count 방식만 지원합니다."
            )

        counter: Counter[str] = Counter()

        for question in self.quiz.questions:
            answer_choice_id = answers.get(question.id)
            if answer_choice_id is None:
                continue

            for choice in question.choices:
                if choice.id == answer_choice_id:
                    counter[choice.result_type] += 1
                    break

        # 모든 결과 유형을 포함하여 반환 (0점 포함)
        result = {}
        for result_type in self.quiz.results.keys():
            result[result_type] = counter.get(result_type, 0)

        return result
