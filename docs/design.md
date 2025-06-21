# 웹 서비스 설계서 v1.0

## 1. 개요
본 문서는 베이비붐 세대(50–66세)를 대상으로 한 심리테스트 웹 서비스(이하 "서비스")의 설계 방안을 기술한다. 서비스 구현 전 **TDD(Test-Driven Development)**, **SOLID 원칙**, **Clean Architecture**를 준수하여 코드 품질과 유지 보수성을 확보한다.

## 2. 개발 원칙 및 프로세스
1. **TDD 사이클**: `Red → Green → Refactor` 순으로 모든 기능을 테스트 코드부터 작성한다.
2. **SOLID**: 각 계층·모듈 설계 시 단일 책임, 개방-폐쇄, 리스코프 치환, 인터페이스 분리, 의존 역전 원칙을 적용한다.
3. **Clean Architecture**: 
   - 외부 의존성(웹 프레임워크, DB, SDK 등)은 가장 바깥 계층에 위치한다.
   - 내부 계층(**Service**)는 Infrastructure(데이터베이스·외부 SDK) 쪽으로만 의존하며, 반대 방향 의존은 금지한다.
4. **Git 커밋**: [Conventional Commits](https://www.conventionalcommits.org/ko/) 규칙을 따른다.

```text
feat: Quiz 도메인 모델 추가
fix(db): answers.result_type 제약 조건 수정
refactor(api): /submit 서비스 객체 리팩터링
```

## 3. 기술 스택
| 레이어 | 기술 | 비고 |
|--------|------|------|
| Presentation | FastAPI, Jinja2, HTMX, TailwindCSS CDN | 다국어 대응 준비 |
| Service | Python 3.11, Pydantic v2 | 비즈니스 로직·유스케이스 |
| Infrastructure | SQLite(aiosqlite) → Supabase(PostgreSQL) | raw SQL → 추후 ORM 전환 |
| Ads | Kakao AdFit, Google AdSense | Stub → 2차 스프린트 실제 SDK |
| CI/CD | GitHub Actions → Render Deploy | `uv run -m pytest` 자동 테스트 |
| 테스트 | pytest, Playwright | 단위·E2E |

## 4. 시스템 아키텍처
```
[Client]
   ↓ HTMX
[Presentation(FastAPI + Jinja2)]
   ↓
[Service Layer]  ← 비즈니스 로직·유스케이스
   ↑
[Infrastructure] ← DB, 외부 SDK(Kakao, AdFit, AdSense, GA4)
```
- **의존성 방향**: 바깥 → 안쪽으로만. Domain은 어떤 라이브러리에도 의존하지 않는다.
- **Boundary**: 인터페이스(Protocol)로 계층 간 통신. 예: `AnswerRepository`, `ResultTypeCalculator`.

## 5. 디렉토리 구조(예시)
```text
nojam/
 ├── nojam/
 │   ├── services/
 │   │   └── quiz.py        # 계산 로직·유스케이스
 │   ├── db/
 │   │   └── repository.py  # raw SQL + aiosqlite
 │   ├── web/
 │   │   ├── templates/
 │   │   └── static/
 │   ├── external/
 │   │   └── kakao_stub.py  # SDK Stub
 │   │   └── adsense_stub.py  # Google AdSense Stub
 │   └── main.py
 ├── tests/
 │   └── e2e/
 ├── pyproject.toml
 └── README.md
```

## 6. 데이터 모델
```sql
CREATE TABLE answers (
  id          TEXT PRIMARY KEY,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  answers_json TEXT NOT NULL,
  result_type TEXT CHECK(result_type IN (
    '7080','IMF','ACT','DRM','PHONE','ANA','TREND','JUNK'
  )),
  ua_hash     CHAR(64)
);
```
- **Salt 교체**: 서비스 기동 시점에 `.env`에서 SALT 값을 읽어 14일마다 rotate.
- **ORM**: SQLModel `Answer` 모델 매핑.

## 7. API 설계
| Method | Path | 설명 | Request | Response |
|--------|------|------|---------|----------|
| GET | /quiz | 첫 문항 HTML 반환(HTMX) | – | 200 HTML |
| POST | /quiz/answer | 한 문항 선택 결과 저장 | `{{question_id, choice}}` | 204 No Content(HTMX swap) |
| POST | /submit | 10문항 제출 → 결과 계산 | `FormData` | 302 /result/{rid} |
| GET | /result/{rid} | 결과 카드 렌더 | – | 200 HTML + OG 태그 |
| GET | /export | 어드민 CSV 다운로드 | `?from=&to=` | 200 CSV |

## 8. 테스트 전략
### 8.1 단위(Unit)
* Service 레이어: `calculate_result_type()` 입력 10개 → 예상 유형 검증.
* Repository mock을 사용하여 Service 테스트.

### 8.2 E2E(Playwright)
* 사용자는 10문항 답 → 결과 카드 확인 → 카카오톡 공유 버튼 클릭 시 SDK 로딩까지.
* **광고 슬롯 렌더**: 결과 페이지 하단 Google AdSense Stub가 정상적으로 호출되는지 확인.

### 8.3 테스트 커버리지 목표
- **단위 70 %+, E2E 50 %+**
- GitHub Actions에서 `pytest --cov` 실패 시 머지 차단.

## 9. 배포 & CI/CD
1. **GitHub Actions**
   - `push`/`pull_request` 이벤트: `uv run -m pytest && playwright install --with-deps`.
   - main 브랜치 머지 시 Render Deploy Hook 호출.
2. **Render**
   - Dockerfile 기반 `uvicorn nojam.main:app --host 0.0.0.0 --port 8000`.
3. **환경변수 관리**: `.env` → Render Dashboard Secret.

## 10. 코드 품질 & 스타일
- **ruff**: 포맷 + 린트 통합.
- **mypy**: 정적 타입 검사(Strict 모드).
- **pre-commit**: 커밋 전 lint·type check 실행.

## 11. 로깅 & 모니터링
- **structlog**: JSON 로그 → Render Log Stream.
- **GA4**: `result_generated` 이벤트 전송.
- **광고 지표**: AdFit·AdSense RPM/CTR 수집.
- **Supabase Row Level Security**: UA 해시 조회 시 개인 식별 불가.

## 12. 향후 확장
1. Supabase로 DB 마이그레이션 후 다중 AZ.
2. 결과 유형별 맞춤 뉴스레터(카카오 비즈메시지).
3. 프리미엄 리포트 구독: Stripe Billing 연동.

---
**문서 변경 이력**
| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| 1.0 | 2025-06-21 | o3-assistant | 최초 작성 | 