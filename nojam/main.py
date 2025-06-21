from fastapi import FastAPI

app = FastAPI(title="Nojam Psych Test API", version="0.1.0")

from nojam.web.routes import router as web_router  # noqa: E402

app.include_router(web_router)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """헬스 체크 엔드포인트."""
    return {"status": "ok"}


# CLI 실행 지원
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("nojam.main:app", host="0.0.0.0", port=8000, reload=True)
