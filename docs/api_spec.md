# API 명세서 v0.1.0

## 개요
베이비붐 세대 대상 심리테스트 웹 서비스의 REST API 명세서입니다.

## 기본 정보
- **Base URL**: `https://nojam.onrender.com` (배포 환경)
- **로컬 개발**: `http://localhost:8000`
- **API 버전**: v0.1.0
- **Content-Type**: `application/json` (API), `text/html` (웹 페이지)

## 엔드포인트

### 1. 퀴즈 관련

#### GET /quiz
퀴즈 페이지를 반환합니다.

**응답**
- **200 OK**: HTML 페이지 (10문항 폼)
- **Content-Type**: `text/html`

**응답 예시**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <title>심리테스트 – 질문</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <!-- 10문항 폼 -->
</body>
</html>
```

#### POST /submit
퀴즈 답변을 제출하고 결과를 계산합니다.

**요청**
- **Content-Type**: `application/x-www-form-urlencoded`
- **Body**: 폼 데이터

**요청 예시**
```
q1=A&q2=B&q3=C&q4=D&q5=A&q6=B&q7=C&q8=D&q9=A&q10=B
```

**응답**
- **302 Found**: 결과 페이지로 리다이렉트
- **Location**: `/result/{answer_id}`

#### GET /result/{answer_id}
특정 답변의 결과 페이지를 반환합니다.

**경로 매개변수**
- `answer_id` (string): 답변 고유 ID (UUID)

**응답**
- **200 OK**: HTML 결과 페이지
- **404 Not Found**: 존재하지 않는 답변 ID

**응답 예시**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <title>심리테스트 결과</title>
  <meta property="og:title" content="나는 7080 감성형!" />
  <meta property="og:image" content="/static/cards/7080.jpg" />
</head>
<body>
  <!-- 결과 카드, 광고 슬롯, 공유 버튼 -->
</body>
</html>
```

### 2. 외부 SDK Stub

#### POST /stub/kakao/share
카카오톡 공유 기능을 시뮬레이션합니다.

**요청**
- **Content-Type**: `application/json`

**요청 예시**
```json
{
  "result_id": "abc123",
  "result_type": "7080"
}
```

**응답**
- **200 OK**: 공유 성공

**응답 예시**
```json
{
  "status": "ok",
  "shared_result_id": "abc123",
  "timestamp": "2025-01-21T10:30:00Z"
}
```

#### GET /stub/kakao/share
카카오톡 공유 기록을 조회합니다.

**응답**
- **200 OK**: 공유 기록 리스트

**응답 예시**
```json
{
  "shares": [
    {
      "result_id": "abc123",
      "result_type": "7080",
      "timestamp": "2025-01-21T10:30:00Z"
    }
  ]
}
```

#### POST /stub/adsense/render
Google AdSense 광고 렌더링을 시뮬레이션합니다.

**요청**
- **Content-Type**: `application/json`

**요청 예시**
```json
{
  "slot_id": "result-page-bottom",
  "page_url": "/result/abc123"
}
```

**응답**
- **200 OK**: 광고 렌더링 성공

**응답 예시**
```json
{
  "status": "rendered",
  "slot_id": "result-page-bottom",
  "ad_html": "<div>광고 콘텐츠 (Stub)</div>",
  "timestamp": "2025-01-21T10:30:00Z"
}
```

## 데이터 모델

### Answer
```json
{
  "id": "uuid-string",
  "created_at": "2025-01-21T10:30:00Z",
  "answers_json": "{\"q1\":\"A\",\"q2\":\"B\",...}",
  "result_type": "7080",
  "ua_hash": "sha256-hash"
}
```

### 결과 유형
- `7080`: 7080 감성형
- `IMF`: IMF 생존형  
- `ACT`: 운동권 열혈형
- `DRM`: MBC드라마형
- `PHONE`: 폰 적응형
- `ANA`: 아날로그 고수형
- `TREND`: 유행 선도형
- `JUNK`: 정크컬쳐 수집형

## 오류 처리

### HTTP 상태 코드
- **200 OK**: 성공
- **302 Found**: 리다이렉트
- **400 Bad Request**: 잘못된 요청
- **404 Not Found**: 리소스 없음
- **500 Internal Server Error**: 서버 오류

### 오류 응답 형식
```json
{
  "error": {
    "code": "INVALID_QUIZ_ANSWERS",
    "message": "필수 문항이 누락되었습니다.",
    "details": {
      "missing_questions": ["q1", "q5"]
    }
  }
}
```

## 보안

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