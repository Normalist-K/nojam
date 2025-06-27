# 🚀 새로운 심리테스트 추가 가이드

## 개요

이 가이드는 `references/` 폴더에 있는 테스트 자료를 JSON 기반 웹서비스에 자동으로 반영하는 과정을 설명합니다.

## 시스템 구조

```
references/sample_test_x/     →     assets/quizzes/test-x.json     →     웹서비스 자동 반영
├── testx.md (문항 & 결과)
└── cardx.html (결과 카드)
```

## AI 어시스턴트를 위한 표준 프롬프트

### 🎯 완전 자동화 프롬프트

```
references 폴더에 있는 sample_test{X}를 웹서비스에 반영해줘.

**작업 순서:**
1. references/sample_test{X}/test{X}.md 파일 분석
2. test{X}.md의 문항과 결과 유형을 JSON 스키마 v2.1에 맞게 변환
3. assets/quizzes/{테스트명}.json 파일 생성
4. 결과 카드는 이미 card{X}.html로 완성되어 있음 (JSON에 스타일 정보만 포함)

**JSON 변환 규칙:**
- meta.id: 영문 소문자 + 언더스코어 (예: mbti_5060_test)
- 문항은 각 선택지가 특정 결과 유형에 1점씩 배정 (simple_count 방식)
- 결과 유형은 test{X}.md의 "결과유형" 섹션에서 추출
- 각 결과에는 title, subtitle, description, keywords, quote, emoji, style 포함
- **⚠️ 중요**: style 객체는 반드시 다음 필드들을 포함해야 함:
  - gradient: CSS 그라데이션 (linear-gradient로 시작)
  - number: 원형 숫자 (①②③④⑤⑥⑦⑧⑨⑩ 중 하나)
  - css_class: "type-1", "type-2", ... "type-16" 형식 (type-숫자)

**참고 파일:**
- 스키마: assets/schemas/quiz-schema-v2.1.json
- 기존 예시: assets/quizzes/mind-age-test.json, assets/quizzes/conversation-style-test.json

완료 후 "✅ {테스트명} 웹서비스 반영 완료"라고 알려줘.
```

### 🔧 단계별 상세 프롬프트

#### 1단계: 파일 분석
```
references/sample_test{X} 폴더의 구조를 확인하고:
1. test{X}.md에서 문항과 결과 유형 추출
2. card{X}.html에서 스타일 정보 확인
3. JSON 스키마에 맞는 구조로 매핑 계획 수립
```

#### 2단계: JSON 생성
```
test{X}.md 내용을 기반으로 assets/quizzes/{테스트명}.json 생성:
- assets/schemas/quiz-schema-v2.1.json 스키마 준수
- simple_count 점수 방식 사용
- 모든 필드 완전히 채우기 (meta, config, questions, results)
```

#### 3단계: 검증
```
생성된 JSON 파일이 다음 조건을 만족하는지 확인:
- 스키마 유효성
- 문항 수와 config.question_count 일치
- 결과 유형 수와 config.result_types 일치
- 모든 result_type이 results 객체에 정의됨
```

## 파일 구조 및 명명 규칙

### References 폴더 구조
```
references/
└── sample_test{X}/
    ├── test{X}.md          # 문항과 결과 정의
    ├── card{X}.html        # 결과 카드 HTML
    └── README.md           # (선택) 테스트 설명
```

### Assets 폴더 구조
```
assets/
├── quizzes/
│   └── {테스트명}.json     # 새로 생성될 JSON 파일
└── schemas/
    └── quiz-schema-v2.1.json
```

### JSON 파일 명명 규칙
- 영문 소문자 + 하이픈 사용
- 예시: `mbti-5060-test.json`, `conversation-style-test.json`

## JSON 스키마 v2.1 핵심 구조

### 필수 필드
```json
{
  "$schema": "https://nojam.com/schemas/quiz-v2.1.json",
  "meta": {
    "id": "테스트_고유_id",
    "title": "🔹 테스트 제목", 
    "description": "테스트 설명",
    "version": "1.0.0",
    "author": "nojam-team",
    "created_at": "YYYY-MM-DD",
    "estimated_time": "N분",
    "target_age": "연령대"
  },
  "config": {
    "question_count": 문항수,
    "result_types": 결과유형수,
    "scoring_method": "simple_count",
    "randomize_questions": false,
    "show_progress": true
  },
  "questions": [문항 배열],
  "results": {결과 유형 객체},
  "analytics": {
    "enabled": true,
    "events": ["quiz_started", "question_answered", "quiz_completed", "result_shared"]
  }
}
```

### 문항 구조
```json
{
  "id": "q1",
  "text": "질문 내용",
  "type": "single_choice",
  "choices": [
    {
      "id": "q1_a",
      "text": "선택지 텍스트",
      "result_type": "결과유형코드"
    }
  ]
}
```

### 결과 구조
```json
"결과유형코드": {
  "code": "결과유형코드",
  "title": "결과 제목",
  "subtitle": "부제목/한줄평",
  "description": "상세 설명",
  "keywords": ["키워드1", "키워드2", "키워드3"],
  "quote": "대표 문구",
  "emoji": "🔸",
  "style": {
    "gradient": "linear-gradient(...)",
    "css_class": "타입명"
  }
}
```

## 점수 계산 방식

### Simple Count (기본)
- 각 선택지는 하나의 결과 유형에만 1점 부여
- 최다 득점 유형이 최종 결과
- 동점 시 알파벳 순서로 결정

### 결과 유형 매핑 전략
1. **이분법 테스트**: E/I, S/N, T/F, J/P → MBTI 조합
2. **다중 유형**: 직접 매핑 (7080, IMF, ACT 등)
3. **복합 테스트**: 주요 차원별 분류 후 조합

## 자주 발생하는 문제 및 해결

### 🚨 가장 흔한 Pydantic 검증 오류들

#### 1. style.number 필드 누락
```json
// ❌ 잘못된 예시
"style": {
  "gradient": "linear-gradient(...)",
  "css_class": "type-1"
}

// ✅ 올바른 예시  
"style": {
  "gradient": "linear-gradient(...)",
  "number": "①",
  "css_class": "type-1"
}
```

#### 2. css_class 패턴 오류
```json
// ❌ 잘못된 예시
"css_class": "estj"
"css_class": "mbti-type"

// ✅ 올바른 예시
"css_class": "type-1"
"css_class": "type-16"
```

#### 3. gradient 형식 오류
```json
// ❌ 잘못된 예시
"gradient": "background: linear-gradient(...)"

// ✅ 올바른 예시
"gradient": "linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)"
```

### 기타 문제들

#### 4. JSON 스키마 오류
```bash
# 검증 방법
cat assets/quizzes/새파일.json | jq '.' > /dev/null
```

#### 5. 문항 수 불일치
- `config.question_count`와 실제 `questions` 배열 길이 확인
- 누락된 문항이나 중복 ID 점검

#### 6. 결과 유형 참조 오류
- 모든 `result_type`이 `results` 객체에 정의되었는지 확인
- 대소문자 정확성 점검

#### 7. 스타일 정보 누락
- 각 결과에 `style.gradient`, `style.number`, `style.css_class` 모두 필수
- card.html의 CSS 클래스명과 일치 확인

## 성공 체크리스트

### ✅ JSON 파일 생성 완료
- [ ] assets/quizzes/ 폴더에 새 JSON 파일 생성
- [ ] 파일명이 명명 규칙에 부합
- [ ] JSON 문법 오류 없음

### ✅ 스키마 준수
- [ ] 모든 필수 필드 포함
- [ ] 필드 타입과 형식 올바름
- [ ] 배열 길이 제한 준수

### ✅ 데이터 일관성
- [ ] 문항 수 일치
- [ ] 결과 유형 수 일치
- [ ] 모든 result_type 정의됨
- [ ] 선택지 ID 중복 없음

### ✅ 내용 품질
- [ ] 문항 텍스트 자연스러움
- [ ] 결과 설명 완성도
- [ ] 이모지와 스타일 적절성

## 고급 기능

### A/B 테스트
```json
"meta": {
  "id": "test_v2",
  "variant": "A",
  "base_test": "test_v1"
}
```

### 다국어 지원
```json
"meta": {
  "id": "test_en",
  "language": "en",
  "base_test": "test_ko"
}
```

### 가중치 점수 (향후)
```json
"choices": [
  {
    "id": "q1_a",
    "text": "선택지",
    "scores": {
      "TYPE_A": 2,
      "TYPE_B": 1
    }
  }
]
```

---

**📝 마지막 업데이트**: 2025-01-21  
**📋 버전**: v1.0  
**✍️ 작성자**: nojam-team 