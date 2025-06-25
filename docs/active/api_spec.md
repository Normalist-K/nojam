# API 명세서 v0.2.0

## 개요
베이비붐 세대 대상 심리테스트 웹 서비스의 REST API 명세서입니다.
**Phase 1**: JSON 기반 동적 퀴즈 플랫폼 구현 완료

## 기본 정보
- **Base URL**: `https://nojam.onrender.com` (배포 환경)
- **로컬 개발**: `http://localhost:8000`
- **API 버전**: v0.2.0
- **Content-Type**: `application/json` (API), `text/html` (웹 페이지)

## 주요 변경사항 (v0.2.0)
- ✅ **JSON 기반 퀴즈 시스템**: 하드코딩 없이 JSON 파일로 퀴즈 관리
- ✅ **Pydantic v2 마이그레이션**: 최신 Python 표준 적용
- ✅ **동적 퀴즈 로딩**: 다중 퀴즈 지원 및 실시간 로드
- ✅ **확장 가능한 점수 계산**: Simple Count, Weighted Sum, Percentage 방식 지원
- ✅ **하위 호환성**: 기존 하드코딩 로직과 완벽 호환

## 엔드포인트

### 1. 퀴즈 관련

#### GET /quiz
동적 퀴즈 페이지를 반환합니다.

**쿼리 매개변수**
- `quiz_id` (string, optional): 사용할 퀴즈 ID (기본값: "mind-age-test")

**응답**
- **200 OK**: HTML 페이지 (동적 문항 수)
- **Content-Type**: `text/html`

**응답 예시**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <title>🕰️ 나는 어떤 시대형 인간일까?</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <!-- 15문항 동적 폼 (JSON 기반) -->
  <form method="post" action="/submit">
    <input type="hidden" name="quiz_id" value="mind-age-test">
    <!-- 동적 생성된 문항들 -->
  </form>
</body>
</html>
```

#### POST /submit
동적 퀴즈 답변을 제출하고 결과를 계산합니다.

**요청**
- **Content-Type**: `application/x-www-form-urlencoded`
- **Body**: 동적 폼 데이터

**요청 예시 (기존 호환)**
```
q1=A&q2=B&q3=C&q4=D&q5=A&q6=B&q7=C&q8=D&q9=A&q10=B
```

**요청 예시 (JSON 기반)**
```
quiz_id=mind-age-test&q1=q1_a&q2=q2_b&q3=q3_c&...&q15=q15_d
```

**응답**
- **302 Found**: 결과 페이지로 리다이렉트
- **Location**: `/result/{answer_id}`
- **400 Bad Request**: 답변 데이터 부족 또는 잘못된 형식

#### GET /result/{answer_id}
JSON 기반 동적 결과 페이지를 반환합니다.

**경로 매개변수**
- `answer_id` (string): 답변 고유 ID (UUID)

**응답**
- **200 OK**: HTML 결과 페이지 (JSON 기반 동적 카드)
- **404 Not Found**: 존재하지 않는 답변 ID

**응답 예시**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <title>🕰️ 나는 7080 감성형!</title>
  <meta property="og:title" content="나는 7080 감성형!" />
  <meta property="og:description" content="향수와 낭만을 사랑하는 당신..." />
</head>
<body>
  <!-- JSON 기반 동적 결과 카드 -->
  <div class="result-card bg-gradient-to-br from-orange-400 to-red-500">
    <h2>🎵 7080 감성형</h2>
    <p>향수와 낭만을 사랑하는 당신</p>
    <!-- 점수 분포, 키워드, 공유 정보 등 -->
  </div>
</body>
</html>
```

### 2. 새로운 API 엔드포인트 (Phase 1)

#### GET /api/quizzes
사용 가능한 퀴즈 목록을 반환합니다.

**응답**
- **200 OK**: 퀴즈 목록 JSON

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

**경로 매개변수**
- `quiz_id` (string): 퀴즈 ID

**응답**
- **200 OK**: 퀴즈 상세 정보
- **404 Not Found**: 존재하지 않는 퀴즈 ID

**응답 예시**
```json
{
  "meta": {
    "id": "mind_age_test",
    "title": "🕰️ 나는 어떤 시대형 인간일까?",
    "description": "베이비붐 세대를 위한 심리테스트",
    "version": "1.0.0",
    "author": "nojam-team",
    "created_at": "2025-01-21",
    "estimated_time": "3-5분",
    "target_age": "50-70"
  },
  "config": {
    "question_count": 15,
    "result_types": 8,
    "scoring_method": "simple_count",
    "randomize_questions": false,
    "show_progress": true
  },
  "question_count": 15,
  "result_types": ["7080", "IMF", "ACT", "MBC", "PHONE", "ANA", "TREND", "JUNK"]
}
```

### 3. 외부 SDK Stub (기존 유지)

#### POST /stub/kakao/share
카카오톡 공유 기능을 시뮬레이션합니다.

**응답**
- **200 OK**: 공유 성공

**응답 예시**
```json
{
  "status": "ok"
}
```

## 데이터 모델

### Quiz (JSON Schema v2.1)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "meta": {
    "id": "mind_age_test",
    "title": "🕰️ 나는 어떤 시대형 인간일까?",
    "description": "베이비붐 세대를 위한 심리테스트",
    "version": "1.0.0",
    "author": "nojam-team",
    "created_at": "2025-01-21",
    "estimated_time": "3-5분",
    "target_age": "50-70"
  },
  "config": {
    "question_count": 15,
    "result_types": 8,
    "scoring_method": "simple_count",
    "randomize_questions": false,
    "show_progress": true
  },
  "questions": [
    {
      "id": "q1",
      "text": "가장 기억에 남는 시대는?",
      "type": "single_choice",
      "choices": [
        {
          "id": "q1_a",
          "text": "60-70년대 (박정희 시대)",
          "result_type": "7080"
        }
      ]
    }
  ],
  "results": {
    "7080": {
      "title": "7080 감성형",
      "subtitle": "향수와 낭만을 사랑하는 당신",
      "description": "과거의 아름다운 추억을 소중히 여기는 타입입니다.",
      "keywords": ["향수", "낭만", "추억", "감성", "전통"],
      "quote": "옛날이 좋았지~",
      "emoji": "🎵",
      "style": {
        "gradient": "from-orange-400 to-red-500",
        "text_color": "text-white",
        "border_color": "border-orange-300"
      }
    }
  }
}
```

### Answer (확장됨)
```json
{
  "id": "uuid-string",
  "created_at": "2025-01-21T10:30:00Z",
  "answers_json": "{\"q1\":\"q1_a\",\"q2\":\"q2_b\",...}",
  "result_type": "7080",
  "ua_hash": "sha256-hash"
}
```

### 결과 유형 (확장됨)
- `7080`: 7080 감성형 🎵
- `IMF`: IMF 생존형 💪
- `ACT`: 운동권 열혈형 ✊
- `MBC`: MBC드라마형 📺
- `PHONE`: 폰 적응형 📱
- `ANA`: 아날로그 고수형 📻
- `TREND`: 유행 선도형 ✨
- `JUNK`: 정크컬쳐 수집형 🎬

## 점수 계산 시스템

### Simple Count (현재 구현)
각 선택지가 특정 결과 유형에 1점을 추가하는 방식
```python
# 예시: q1_a 선택 → 7080 유형에 +1점
{
  "7080": 5,
  "IMF": 3,
  "ACT": 2,
  # ...
}
```

### Weighted Sum (Phase 2 예정)
선택지별로 가중치를 다르게 적용하는 방식

### Percentage (Phase 2 예정)
백분율 기반 점수 계산 방식

## 기술 스택 업데이트

### Backend
- **Python**: 3.11
- **FastAPI**: 0.110+
- **Pydantic**: 2.6+ (v2 마이그레이션 완료)
- **aiosqlite**: 0.19+ (비동기 SQLite)

### 퀴즈 관리
- **JSON Schema**: v2.1 (검증 및 IDE 지원)
- **파일 기반**: `assets/quizzes/*.json`
- **실시간 로딩**: 파일 변경 감지 및 캐시 무효화

## 오류 처리

### 새로운 오류 코드
- `QUIZ_NOT_FOUND`: 존재하지 않는 퀴즈 ID
- `INVALID_QUIZ_FORMAT`: JSON 스키마 검증 실패
- `SCORING_METHOD_NOT_SUPPORTED`: 지원하지 않는 점수 계산 방식

### 오류 응답 형식
```json
{
  "error": {
    "code": "QUIZ_NOT_FOUND",
    "message": "퀴즈를 찾을 수 없습니다: invalid-quiz-id",
    "details": {
      "quiz_id": "invalid-quiz-id",
      "available_quizzes": ["mind-age-test"]
    }
  }
}
```

## 보안 (기존 유지)

### CSRF 보호
- 모든 POST 요청에는 CSRF 토큰 필요
- HTML 폼에 `csrf_token` 히든 필드 포함

### Rate Limiting
- IP당 분당 60회 요청 제한
- 초과 시 429 Too Many Requests 응답

### 데이터 보호
- 개인 식별 정보 미수집
- UA+IP 해시만 저장 (14일마다 salt 교체)

---

**문서 변경 이력**
| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| 0.1.0 | 2025-01-21 | o3-assistant | v0.1.0 릴리즈 기준 API 명세 작성 |
| 0.2.0 | 2025-01-21 | claude-sonnet | Phase 1 JSON 기반 플랫폼 구현 반영, Pydantic v2 마이그레이션 |