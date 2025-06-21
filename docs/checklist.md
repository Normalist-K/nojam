# 개발 체크리스트 v1.0

본 체크리스트는 **코드 에이전트**(o3-assistant)가 단계별로 구현·테스트·커밋을 수행할 수 있도록 '한 번에 수정 가능한' 단위로 분리되어 있다. 모든 프롬프트는 **한국어**로 전달하며, 파이썬 실행은 `uv run`을 사용한다.

> ✅ 표를 그대로 복사해 프롬프트로 사용해도 무방하며, 각 단계 완료 후 다음 단계로 진행한다.

| # | 개발 단계 | 코드 에이전트에게 줄 프롬프트 (예시) | 완료 후 테스트 & 문서 작업 | 커밋 메시지 예시 |
|---|-----------|------------------------------------|---------------------------|------------------|
| 1 | 초기 스캐폴딩 | `nojam 패키지에 services/db/web/external 구조를 생성하고, main.py에 FastAPI 앱 스켈레톤을 만들어줘.` | `pytest -q`(0 tests), 디렉터리 존재 확인 | `feat: 프로젝트 구조 및 FastAPI 스켈레톤 생성` |
| 2 | 설정/패키지 | `pyproject.toml에 fastapi, uvicorn, aiosqlite, pydantic, pytest, playwright, ruff 추가하고 ruff 설정 파일도 생성해줘.` | `uv run -m pytest -q` green, `ruff --version` 확인 | `chore: 의존성 및 린터 설정` |
| 3 | DB 레이어 | `db/repository.py에 aiosqlite 기반 Answers 테이블 CRUD 구현, 타입 힌트·테스트 작성해줘.` | `tests/unit/test_repository.py` green | `feat(db): aiosqlite 기반 AnswerRepository 구현` |
| 4 | Service 레이어 | `services/quiz.py에 결과 계산 로직 calculate_result_type 구현하고 서비스 테스트 추가.` | `tests/unit/test_quiz_service.py` green | `feat(service): 결과 유형 계산 로직 추가` |
| 5 | 외부 Stub | `external/kakao_stub.py, external/adsense_stub.py에 SDK 호출 mock 작성 및 테스트.` | `tests/unit/test_external.py` green | `feat(external): Kakao·AdSense Stub 추가` |
| 6 | Web 라우트 | `web/routes.py에 /quiz, /submit, /result 엔드포인트 구현 & 템플릿 스켈레톤, 테스트 작성.` | `tests/e2e/test_quiz_flow.py` green | `feat(api): 퀴즈·결과 API 및 템플릿 기본 구성` |
| 7 | 템플릿 UI | `Tailwind CDN 포함 기본 레이아웃, 결과 카드 IMG 슬롯, AdSense div 삽입.` | Playwright: 결과 페이지 광고 div 존재 | `feat(ui): 기본 레이아웃·광고 슬롯 구현` |
| 8 | CI 파이프라인 | `.github/workflows/ci.yml에 ruff+pytest+playwright install 실행 추가.` | GitHub Actions 성공 | `ci: GitHub Actions 파이프라인 추가` |
| 9 | Docker/Render | `Dockerfile(uvicorn)과 render.yaml 작성.` | `docker build .` 성공 | `chore: Docker 및 Render 배포 설정` |
|10 | 로깅/모니터링 | `settings.py에 structlog 구성, GA4·광고 지표 로거 추가.` | 단위 테스트: 로그 포맷 검증 | `feat(logging): structlog & 지표 로깅 설정` |
|11 | 문서 반영 | `/docs에 API 스펙, DB 스키마, 광고 연동 문서 업데이트.` | `git diff docs/` 확인 | `docs: 설계서 및 API 문서 갱신` |
|12 | 최종 E2E | `전체 흐름 E2E 테스트 추가: 퀴즈 → 결과 → 공유 stub 호출 → 광고 div 렌더.` | `uv run pytest -q` all green | `test: 전체 사용자 흐름 E2E 추가` |

## 공통 지침
1. **TDD**: `Red → Green → Refactor` 순으로 진행.  
2. **코드 품질**: ruff 포맷·린트, mypy(strict), 커버리지 목표 **단위 70 %+, E2E 50 %+**.  
3. **커밋 규칙**: [Conventional Commits](https://www.conventionalcommits.org/ko/) 준수, 필요 시 `BREAKING CHANGE:` 추가.  
4. **문서화**: UI·API·DB 등 주요 변경 시 `/docs` 하위 파일 업데이트.  
5. **런타임**: Python 3.11, `uv run`을 통해 모든 명령 실행.  
6. **CI 검사 실패 시** 머지 금지, 원인 해결 후 재시도.  

---
문서 변경 이력  
| 버전 | 날짜 | 작성자 | 설명 |  
|------|------|--------|------|  
| 1.0 | 2025-06-21 | o3-assistant | 최초 작성 | 