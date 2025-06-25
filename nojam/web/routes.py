"""FastAPI 라우트 정의 (/quiz, /submit, /result).

JSON 기반 플랫폼으로 업데이트된 라우트.
동적 퀴즈 로딩과 결과 렌더링을 지원한다.
"""

from __future__ import annotations

import hashlib
import json
import logging
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from nojam.db.repository import AnswerRepository
from nojam.services.loader import get_quiz_loader
from nojam.services.quiz import calculate_result_type, get_score_breakdown

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).parent / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


def get_repo() -> AnswerRepository:
    # 파일 SQLite 저장 (간단히 프로젝트 루트에)
    return AnswerRepository(db_path="nojam.sqlite3")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """퀴즈 선택 홈페이지."""
    try:
        loader = get_quiz_loader()
        available_quizzes = loader.get_available_quizzes()

        # 퀴즈 정보 로드
        quiz_list = []
        for quiz_id in available_quizzes:
            try:
                quiz_data = loader.load_quiz(quiz_id)
                quiz_list.append(
                    {
                        "id": quiz_id,
                        "title": quiz_data.meta.title,
                        "description": quiz_data.meta.description,
                        "question_count": len(quiz_data.questions),
                        "result_count": len(quiz_data.results),
                        "target_age": quiz_data.meta.target_age,
                    }
                )
            except Exception as e:
                logger.warning(f"퀴즈 정보 로드 실패: {quiz_id} - {e}")
                continue

        context = {"quizzes": quiz_list}
        logger.info(f"퀴즈 선택 페이지 로드: {len(quiz_list)}개 퀴즈 사용 가능")

        return templates.TemplateResponse(request, "home.html", context)

    except Exception as e:
        logger.error(f"퀴즈 목록 로드 실패: {e}")
        # 에러 시 기본 퀴즈로 리다이렉트
        return RedirectResponse(url="/quiz?quiz_id=mind-age-test", status_code=302)


@router.get("/quiz", response_class=HTMLResponse)
async def quiz(
    request: Request, quiz_id: str | None = Query(None, description="사용할 퀴즈 ID")
) -> HTMLResponse:
    """동적 퀴즈 폼 렌더."""
    # 사용할 퀴즈 결정
    target_quiz_id = quiz_id or "mind-age-test"

    try:
        loader = get_quiz_loader()
        quiz_data = loader.load_quiz(target_quiz_id)

        context = {
            "quiz": quiz_data,
            "quiz_id": target_quiz_id,
        }

        logger.info(f"퀴즈 폼 렌더: {target_quiz_id} (v{quiz_data.meta.version})")
        return templates.TemplateResponse(request, "quiz.html", context)

    except FileNotFoundError:
        logger.error(f"퀴즈 파일을 찾을 수 없음: {target_quiz_id}")
        # 기본 하드코딩된 폼으로 폴백
        return templates.TemplateResponse(
            request, "quiz.html", {"quiz": None, "quiz_id": None}
        )
    except Exception as e:
        logger.error(f"퀴즈 로드 실패: {target_quiz_id} - {e}")
        # 기본 하드코딩된 폼으로 폴백
        return templates.TemplateResponse(
            request, "quiz.html", {"quiz": None, "quiz_id": None}
        )


@router.post("/submit")
async def submit(
    request: Request,
    repo: AnswerRepository = Depends(get_repo),
    quiz_id: str | None = Form(None),
    # 동적 폼 필드 처리를 위해 Form 데이터를 직접 파싱
):
    """동적 퀴즈 제출 처리."""
    form_data = await request.form()

    # quiz_id 추출
    target_quiz_id = form_data.get("quiz_id") or quiz_id

    # 답변 데이터 추출 (q1, q2, ... 또는 동적 필드)
    answers: dict[str, str] = {}

    # 기존 하드코딩된 형식 지원
    for i in range(1, 11):
        field_name = f"q{i}"
        if field_name in form_data:
            answers[field_name] = form_data[field_name]

    # JSON 기반 동적 필드 지원
    if target_quiz_id:
        try:
            loader = get_quiz_loader()
            quiz_data = loader.load_quiz(target_quiz_id)

            # 퀴즈 정의에 따른 필드 추출
            for question in quiz_data.questions:
                qid = question.id
                if qid in form_data:
                    answers[qid] = form_data[qid]

        except Exception as e:
            logger.warning(f"동적 퀴즈 처리 실패, 기존 방식 사용: {e}")

    if not answers:
        raise HTTPException(status_code=400, detail="답변 데이터가 없습니다.")

    # 결과 계산
    try:
        result_type = calculate_result_type(answers, target_quiz_id)
        logger.info(f"결과 계산 완료: {result_type} (퀴즈: {target_quiz_id})")
    except Exception as e:
        logger.error(f"결과 계산 실패: {e}")
        raise HTTPException(status_code=400, detail=f"결과 계산 실패: {e}")

    # 답변 저장
    answer_id = str(uuid.uuid4())
    ua_hash = hashlib.sha256(request.headers.get("user-agent", "").encode()).hexdigest()

    await repo.init()
    await repo.add(
        id=answer_id,
        answers_json=answers,
        result_type=result_type,
        quiz_id=target_quiz_id or "mind-age-test",
        ua_hash=ua_hash,
    )
    await repo.close()

    return RedirectResponse(url=f"/result/{answer_id}", status_code=302)


@router.post("/stub/kakao/share")
async def kakao_share_stub():
    """카카오톡 공유 스텁."""
    from nojam.external.kakao_stub import share_link

    share_link("테스트", "https://example.com")
    return {"status": "ok"}


@router.get("/result/{answer_id}", response_class=HTMLResponse)
async def result(
    answer_id: str, request: Request, repo: AnswerRepository = Depends(get_repo)
) -> HTMLResponse:
    """결과 페이지 렌더 (JSON 기반 카드 포함)."""
    await repo.init()
    record = await repo.get(answer_id)
    await repo.close()

    if record is None:
        raise HTTPException(status_code=404, detail="결과를 찾을 수 없습니다.")

    result_type = record["result_type"]
    answers = json.loads(record["answers_json"])
    quiz_id = record.get("quiz_id", "mind-age-test")

    # 결과 상세 정보 로드
    result_details = None
    score_breakdown = None
    quiz_data = None

    try:
        # 저장된 퀴즈 ID로 결과 정보 로드
        loader = get_quiz_loader()
        quiz_data = loader.load_quiz(quiz_id)

        if result_type in quiz_data.results:
            result_details = quiz_data.results[result_type]

        # 점수 분포 계산
        score_breakdown = get_score_breakdown(answers, quiz_id)

        logger.info(f"결과 상세 로드 완료: {result_type} (퀴즈: {quiz_id})")

    except Exception as e:
        logger.warning(f"JSON 기반 결과 로드 실패, 기본 정보만 표시: {e}")

        # 폴백: 기본 퀴즈로 시도
        try:
            quiz_data = loader.load_quiz("mind-age-test")
            if result_type in quiz_data.results:
                result_details = quiz_data.results[result_type]
            score_breakdown = get_score_breakdown(answers, "mind-age-test")
        except Exception:
            pass

    context = {
        "result_type": result_type,
        "answers": answers,
        "result_details": result_details,
        "score_breakdown": score_breakdown,
        "quiz": quiz_data,
    }

    return templates.TemplateResponse(request, "result.html", context)


@router.get("/api/quizzes")
async def list_quizzes():
    """사용 가능한 퀴즈 목록 API."""
    try:
        loader = get_quiz_loader()
        quiz_ids = loader.get_available_quizzes()

        quizzes = []
        for quiz_id in quiz_ids:
            try:
                quiz_data = loader.load_quiz(quiz_id)
                quizzes.append(
                    {
                        "id": quiz_id,
                        "title": quiz_data.meta.title,
                        "description": quiz_data.meta.description,
                        "version": quiz_data.meta.version,
                        "question_count": quiz_data.config.question_count,
                        "result_types": quiz_data.config.result_types,
                    }
                )
            except Exception as e:
                logger.warning(f"퀴즈 {quiz_id} 로드 실패: {e}")

        return {"quizzes": quizzes}

    except Exception as e:
        logger.error(f"퀴즈 목록 조회 실패: {e}")
        return {"quizzes": [], "error": str(e)}


@router.get("/api/quiz/{quiz_id}")
async def get_quiz_info(quiz_id: str):
    """특정 퀴즈 정보 API."""
    try:
        loader = get_quiz_loader()
        quiz_data = loader.load_quiz(quiz_id)

        return {
            "meta": quiz_data.meta.model_dump(),
            "config": quiz_data.config.model_dump(),
            "question_count": len(quiz_data.questions),
            "result_types": list(quiz_data.results.keys()),
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"퀴즈를 찾을 수 없습니다: {quiz_id}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"퀴즈 로드 실패: {e}")
