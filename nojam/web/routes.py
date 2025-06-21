"""FastAPI 라우트 정의 (/quiz, /submit, /result)."""
from __future__ import annotations

import hashlib
import json
import uuid
from pathlib import Path
from typing import Annotated, Dict

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from nojam.db.repository import AnswerRepository
from nojam.services.quiz import calculate_result_type

TEMPLATES_DIR = Path(__file__).parent / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


def get_repo() -> AnswerRepository:
    # 파일 SQLite 저장 (간단히 프로젝트 루트에)
    return AnswerRepository(db_path="nojam.sqlite3")


@router.get("/quiz", response_class=HTMLResponse)
async def quiz(request: Request) -> HTMLResponse:
    """10문항 폼 렌더."""
    return templates.TemplateResponse("quiz.html", {"request": request})


@router.post("/submit")
async def submit(
    q1: Annotated[str, Form()],
    q2: Annotated[str, Form()],
    q3: Annotated[str, Form()],
    q4: Annotated[str, Form()],
    q5: Annotated[str, Form()],
    q6: Annotated[str, Form()],
    q7: Annotated[str, Form()],
    q8: Annotated[str, Form()],
    q9: Annotated[str, Form()],
    q10: Annotated[str, Form()],
    request: Request,
    repo: AnswerRepository = Depends(get_repo),
):
    answers: Dict[str, str] = {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "q5": q5,
        "q6": q6,
        "q7": q7,
        "q8": q8,
        "q9": q9,
        "q10": q10,
    }

    result_type = calculate_result_type(answers)

    answer_id = str(uuid.uuid4())
    ua_hash = hashlib.sha256(request.headers.get("user-agent", "").encode()).hexdigest()

    # 저장
    await repo.init()
    await repo.add(id=answer_id, answers_json=answers, result_type=result_type, ua_hash=ua_hash)
    await repo.close()

    return RedirectResponse(url=f"/result/{answer_id}", status_code=302)


@router.post("/stub/kakao/share")
async def kakao_share_stub():
    from nojam.external.kakao_stub import share_link

    share_link("테스트", "https://example.com")
    return {"status": "ok"}


@router.get("/result/{answer_id}", response_class=HTMLResponse)
async def result(answer_id: str, request: Request, repo: AnswerRepository = Depends(get_repo)) -> HTMLResponse:
    await repo.init()
    record = await repo.get(answer_id)
    await repo.close()
    if record is None:
        raise HTTPException(status_code=404, detail="결과를 찾을 수 없습니다.")

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "result_type": record["result_type"],
            "answers": json.loads(record["answers_json"]),
        },
    )
