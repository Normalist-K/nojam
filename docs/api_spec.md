# API 스펙 v1.0

본 문서는 현재 FastAPI 애플리케이션에서 제공하는 REST/HTML 엔드포인트의 사양을 정리한 것이다. 실제 코드(`nojam/web/routes.py`, `nojam/main.py`)와 동기화되어 있으며, 변경 시 반드시 이 문서를 갱신한다.

## 공통
- **기본 URL**: `https://<domain>`
- **응답 포맷**: HTML(Form 렌더링) 또는 JSON(Stub-API)  
  (`Content-Type` 기준)
- **상태 코드 규칙**: 성공 2xx, 리다이렉트 3xx, 클라이언트 오류 4xx, 서버 오류 5xx.

---

## 엔드포인트 목록

| Method | Path | 설명 | 요청 파라미터 | 응답 | 상태 코드 |
|--------|------|------|---------------|-------|-----------|
| GET | `/quiz` | 10문항 폼 첫 화면 렌더 | – | HTML | 200 |
| POST | `/submit` | 10문항 제출 → 결과 계산·DB 저장 → 리다이렉트 | `Form(q1–q10)` | Redirect(`/result/{id}`) | 302 |
| GET | `/result/{id}` | 결과 카드 & 공유·광고 슬롯 렌더 | Path `id: UUID` | HTML | 200 / 404 |
| POST | `/stub/kakao/share` | Kakao 공유 Stub 호출 | body: `{}` | `{"status":"ok"}` | 200 |
| GET | `/health` | 헬스 체크 | – | `{"status": "ok"}` | 200 |

---

## 상세 정의

### 1. GET /quiz
- **설명**: Jinja2 템플릿 `quiz.html`을 렌더하여 첫 질문을 표시한다.
- **HTMX 사용**: 각 질문 제출 시 HTMX `hx-post="/quiz/answer"`(향후 구현)로 다음 질문을 스왑.

### 2. POST /submit
- **Form 필드**: `q1` … `q10` (문자열, 각 선택지 코드)
- **서버 로직**:
  1. 10개 답변 dict 구성
  2. `calculate_result_type()` 호출하여 8종 중 결과 타입 반환
  3. UUID 생성 → `answers` 테이블에 저장
  4. `/result/{uuid}`로 302 리다이렉트

```
# 요청 (x-www-form-urlencoded)
q1=D&q2=A&...&q10=B

# 응답 헤더 예시
HTTP/1.1 302 Found
Location: /result/3b7c7c0c-b1d1-4c14-9c1e-a59f1ebde00e
```

### 3. GET /result/{id}
- **설명**: 결과 카드(`result.html`)를 렌더하고 OG 태그, 광고 div, 카카오 공유 버튼을 포함한다.
- **Path 변수**: `id` – UUID, primary key of `answers`.
- **오류**: 존재하지 않는 `id`이면 404.

### 4. POST /stub/kakao/share
- **용도**: 테스트 환경에서 Kakao JS SDK 대신 호출 이력을 남김.
- **응답 JSON**: `{ "status": "ok" }`

### 5. GET /health
간단한 상태 확인용. Render health check에서도 사용.

---

## OpenAPI 스니펫(자동 생성)
FastAPI는 `/openapi.json`, `Swagger UI(/docs)`, `ReDoc(/redoc)`을 자동 제공한다. CI 파이프라인에서 이 JSON을 export ➜ Stoplight 등 API 문서 툴에 업로드하는 플랜을 검토 중이다. 