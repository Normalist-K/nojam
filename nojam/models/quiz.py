"""Quiz models for JSON-driven platform.

Pydantic models that match the JSON Schema v2.1 structure.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator


class ScoringMethod(str, Enum):
    """점수 계산 방식."""

    SIMPLE_COUNT = "simple_count"
    WEIGHTED_SUM = "weighted_sum"
    PERCENTAGE = "percentage"


class QuestionType(str, Enum):
    """문항 유형."""

    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    SLIDER = "slider"
    RANKING = "ranking"


class QuizMeta(BaseModel):
    """테스트 메타데이터."""

    id: str = Field(..., pattern=r"^[a-z0-9_-]+$", description="테스트 고유 ID")
    title: str = Field(..., min_length=1, max_length=100, description="테스트 제목")
    description: str = Field(
        ..., min_length=1, max_length=500, description="테스트 설명"
    )
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$", description="버전")
    author: Optional[str] = Field(None, description="작성자")
    created_at: Optional[date] = Field(None, description="생성일")
    estimated_time: Optional[str] = Field(None, description="예상 소요 시간")
    target_age: Optional[str] = Field(None, description="대상 연령")


class QuizConfig(BaseModel):
    """테스트 설정."""

    question_count: int = Field(..., ge=1, le=50, description="문항 수")
    result_types: int = Field(..., ge=2, le=20, description="결과 유형 수")
    scoring_method: ScoringMethod = Field(..., description="점수 계산 방식")
    randomize_questions: bool = Field(False, description="문항 순서 랜덤화")
    show_progress: bool = Field(True, description="진행률 표시")


class Choice(BaseModel):
    """선택지."""

    id: str = Field(..., pattern=r"^q\d+_[a-z]$", description="선택지 ID")
    text: str = Field(..., min_length=1, max_length=100, description="선택지 텍스트")
    result_type: str = Field(..., pattern=r"^[A-Z0-9_]+$", description="결과 유형")


class Question(BaseModel):
    """문항."""

    id: str = Field(..., pattern=r"^q\d+$", description="문항 ID")
    text: str = Field(..., min_length=1, max_length=200, description="문항 텍스트")
    type: QuestionType = Field(..., description="문항 유형")
    choices: List[Choice] = Field(
        ..., min_items=2, max_items=10, description="선택지 목록"
    )

    @validator("choices")
    def validate_choices(cls, v, values):
        """선택지 ID가 문항 ID와 일치하는지 검증."""
        if "id" in values:
            question_id = values["id"]
            for choice in v:
                if not choice.id.startswith(f"{question_id}_"):
                    raise ValueError(
                        f"선택지 ID {choice.id}가 문항 ID {question_id}와 일치하지 않습니다"
                    )
        return v


class ResultStyle(BaseModel):
    """결과 카드 스타일."""

    gradient: str = Field(
        ..., pattern=r"^linear-gradient\(", description="CSS 그라데이션"
    )
    number: str = Field(..., pattern=r"^[①②③④⑤⑥⑦⑧⑨⑩]$", description="원형 숫자")
    css_class: str = Field(..., pattern=r"^type-\d+$", description="CSS 클래스명")


class ShareInfo(BaseModel):
    """공유 정보."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=100, description="공유 제목"
    )
    description: Optional[str] = Field(
        None, min_length=1, max_length=200, description="공유 설명"
    )
    hashtags: Optional[List[str]] = Field(None, description="해시태그")


class Result(BaseModel):
    """결과 유형."""

    code: str = Field(..., pattern=r"^[A-Z0-9_]+$", description="결과 유형 코드")
    title: str = Field(..., min_length=1, max_length=50, description="결과 제목")
    subtitle: str = Field(..., min_length=1, max_length=100, description="결과 부제목")
    description: str = Field(..., min_length=1, max_length=500, description="결과 설명")
    keywords: List[str] = Field(
        ..., min_items=1, max_items=5, description="대표 키워드"
    )
    quote: str = Field(..., min_length=1, max_length=100, description="대표 대사")
    emoji: str = Field(..., description="대표 이모지")
    style: ResultStyle = Field(..., description="카드 스타일 정보")
    share: Optional[ShareInfo] = Field(None, description="공유 정보")


class Analytics(BaseModel):
    """분석 설정."""

    enabled: bool = Field(True, description="분석 활성화")
    events: Optional[List[str]] = Field(None, description="추적할 이벤트")


class Quiz(BaseModel):
    """완전한 퀴즈 정의."""

    schema_: Optional[str] = Field(
        None, alias="$schema", description="JSON Schema 참조"
    )
    meta: QuizMeta = Field(..., description="테스트 메타데이터")
    config: QuizConfig = Field(..., description="테스트 설정")
    questions: List[Question] = Field(..., min_items=1, description="문항 목록")
    results: Dict[str, Result] = Field(
        ..., min_properties=2, description="결과 유형 정의"
    )
    analytics: Optional[Analytics] = Field(None, description="분석 설정")

    @validator("questions")
    def validate_question_count(cls, v, values):
        """문항 수가 config와 일치하는지 검증."""
        if "config" in values:
            expected_count = values["config"].question_count
            if len(v) != expected_count:
                raise ValueError(
                    f"문항 수가 일치하지 않습니다: 설정={expected_count}, 실제={len(v)}"
                )
        return v

    @validator("results")
    def validate_result_types(cls, v, values):
        """결과 유형 수가 config와 일치하는지 검증."""
        if "config" in values:
            expected_count = values["config"].result_types
            if len(v) != expected_count:
                raise ValueError(
                    f"결과 유형 수가 일치하지 않습니다: 설정={expected_count}, 실제={len(v)}"
                )
        return v

    @validator("results")
    def validate_result_codes(cls, v, values):
        """모든 선택지의 result_type이 results에 정의되어 있는지 검증."""
        if "questions" in values:
            defined_types = set(v.keys())
            used_types = set()

            for question in values["questions"]:
                for choice in question.choices:
                    used_types.add(choice.result_type)

            undefined_types = used_types - defined_types
            if undefined_types:
                raise ValueError(f"정의되지 않은 결과 유형: {undefined_types}")

        return v

    class Config:
        allow_population_by_field_name = True
