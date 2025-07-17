# API 명세서 v0.2.0 (완료)

## 개요
베이비붐 세대 대상 심리테스트 웹 서비스의 REST API 명세서입니다.
**Phase 1**: JSON 기반 동적 퀴즈 플랫폼 구현 완료 ✅

## 기본 정보
- **Base URL**: `https://nojam.onrender.com` (배포 환경)
- **로컬 개발**: `http://localhost:8000`
- **API 버전**: v0.2.0
- **Content-Type**: `application/json` (API), `text/html` (웹 페이지)

## 주요 변경사항 (v0.2.0) - 완료됨
- ✅ **JSON 기반 퀴즈 시스템**: 하드코딩 없이 JSON 파일로 퀴즈 관리
- ✅ **Pydantic v2 마이그레이션**: 최신 Python 표준 적용
- ✅ **동적 퀴즈 로딩**: 다중 퀴즈 지원 및 실시간 로드
- ✅ **확장 가능한 점수 계산**: Simple Count, MBTI Dimensions 방식 지원
- ✅ **하위 호환성**: 기존 하드코딩 로직과 완벽 호환
- ✅ **FastAPI 기반 라우팅**: 모든 엔드포인트 구현 완료

## 구현된 엔드포인트

### 1. 웹 페이지 엔드포인트

#### GET /
퀴즈 선택 홈페이지를 반환합니다.
- **구현 위치**: `nojam/web/routes.py:home()`
- **기능**: 사용 가능한 퀴즈 목록 표시
- **템플릿**: `templates/home.html`

**응답**
- **200 OK**: HTML 페이지 (퀴즈 목록)
- **302 Found**: 에러 시 기본 퀴즈로 리다이렉트

#### GET /quiz
동적 퀴즈 페이지를 반환합니다.
- **구현 위치**: `nojam/web/routes.py:quiz()`
- **기능**: JSON 기반 동적 퀴즈 폼 렌더링

**쿼리 매개변수**
- `quiz_id` (string, optional): 사용할 퀴즈 ID (기본값: "mind-age-test")

**응답**
- **200 OK**: HTML 페이지 (동적 문항 수)
- **Content-Type**: `text/html`

#### POST /submit
동적 퀴즈 답변을 제출하고 결과를 계산합니다.
- **구현 위치**: `nojam/web/routes.py:submit()`
- **기능**: 폼 데이터 파싱, 점수 계산, DB 저장

**요청**
- **Content-Type**: `application/x-www-form-urlencoded`
- **Body**: 동적 폼 데이터

**응답**
- **302 Found**: 결과 페이지로 리다이렉트
- **Location**: `/result/{answer_id}`
- **400 Bad Request**: 답변 데이터 부족 또는 잘못된 형식

#### GET /result/{answer_id}
JSON 기반 동적 결과 페이지를 반환합니다.
- **구현 위치**: `nojam/web/routes.py:result()`
- **기능**: 결과 카드 동적 생성, 점수 분포 표시

**경로 매개변수**
- `answer_id` (string): 답변 고유 ID (UUID)

**응답**
- **200 OK**: HTML 결과 페이지 (JSON 기반 동적 카드)
- **404 Not Found**: 존재하지 않는 답변 ID

### 2. API 엔드포인트

#### GET /api/quizzes
사용 가능한 퀴즈 목록을 반환합니다.
- **구현 위치**: `nojam/web/routes.py:list_quizzes()`

**응답 예시**
```json
{
  "quizzes": [
    {
      "id": "mind-age-test",
      "title": "🕰️ 나는 어떤 시대형 인간일까?",
      "description": "베이비붐 세대를 위한 심리테스트",
      "version": "1.0.0",
      "question_count": 15,
      "result_types": 8
    }
  ]
}
```

#### GET /api/quiz/{quiz_id}
특정 퀴즈의 상세 정보를 반환합니다.
- **구현 위치**: `nojam/web/routes.py:get_quiz_info()`

**경로 매개변수**
- `quiz_id` (string): 퀴즈 ID

**응답**
- **200 OK**: 퀴즈 상세 정보
- **404 Not Found**: 존재하지 않는 퀴즈 ID

#### POST /stub/kakao/share
카카오톡 공유 기능을 시뮬레이션합니다.
- **구현 위치**: `nojam/web/routes.py:kakao_share_stub()`

**응답**
```json
{
  "status": "ok"
}
```

#### GET /health
헬스 체크 엔드포인트입니다.
- **구현 위치**: `nojam/main.py:health()`

**응답**
```json
{
  "status": "ok"
}
```

## 구현된 서비스 모듈

### Quiz Loader
- **파일**: `nojam/services/loader.py`
- **기능**: JSON 파일 동적 로딩, 캐시 관리, 파일 변경 감지

### Quiz Service
- **파일**: `nojam/services/quiz.py`
- **기능**: 결과 계산, 점수 분포 계산

### Scoring Engine
- **파일**: `nojam/services/scoring.py`
- **기능**: 다양한 점수 계산 방식 지원

### Repository
- **파일**: `nojam/db/repository.py`
- **기능**: SQLite 데이터베이스 접근, CRUD 연산

## 데이터 모델

### Quiz (Pydantic v2)
- **파일**: `nojam/models/quiz.py`
- **기능**: JSON Schema v2.1 완전 지원
- **특징**: 강력한 데이터 검증, 타입 안정성

### 지원되는 점수 계산 방식
1. **Simple Count**: 기본 방식, 각 선택지 1점
2. **MBTI Dimensions**: 4차원 독립 계산 후 조합
3. **Weighted Sum**: 향후 구현 예정
4. **Percentage**: 향후 구현 예정

## 템플릿 시스템

### 구현된 템플릿
- `templates/base.html`: 기본 레이아웃
- `templates/home.html`: 퀴즈 선택 페이지
- `templates/quiz.html`: 동적 퀴즈 폼
- `templates/result.html`: 결과 페이지

### 동적 기능
- 가변 문항 수 지원
- JSON 기반 카드 스타일
- TailwindCSS 그라데이션
- 반응형 디자인

## 에러 처리

### 구현된 에러 처리
- JSON 파일 로드 실패 시 폴백
- 잘못된 quiz_id 처리
- 데이터베이스 연결 실패 처리
- 점수 계산 실패 처리

## 성능 최적화

### 구현된 최적화
- 퀴즈 파일 메모리 캐싱
- 파일 변경 감지 후 재로드
- 싱글턴 패턴 로더
- 비동기 데이터베이스 접근

---

**문서 변경 이력**
| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| 0.1.0 | 2025-01-21 | o3-assistant | 초기 API 명세서 작성 |
| 0.2.0 | 2025-01-21 | claude-sonnet | Phase 1 구현 완료 반영, 실제 구현 내용 반영 |