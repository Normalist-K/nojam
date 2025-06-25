# JSON-Driven 심리테스트 플랫폼 로드맵 v2.1

## 1. 개요

### 1.1 목표
- **내부 테스트 제작 플랫폼**: 외부 사용자 업로드가 아닌, 내부 팀이 다양한 심리테스트를 빠르게 제작·배포할 수 있는 시스템
- **JSON 기반 콘텐츠 관리**: 코드 수정 없이 JSON 파일만으로 새로운 심리테스트 생성
- **확장 가능한 아키텍처**: 향후 다양한 테스트 형식과 결과 유형을 지원할 수 있는 유연한 구조

### 1.2 핵심 가치
- **빠른 반복**: 새로운 심리테스트 아이디어를 1시간 내에 웹에 배포
- **일관된 UX**: 모든 테스트가 동일한 디자인 시스템과 사용자 경험 제공
- **데이터 통합**: 모든 테스트 결과를 통합 대시보드에서 분석
- **A/B 테스트 지원**: 동일 테스트의 여러 버전을 동시에 운영하여 최적화

## 2. 아키텍처 설계

### 2.1 전체 구조
```
┌─────────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Content Layer     │    │   Service Layer  │    │   Data Layer    │
│                     │    │                  │    │                 │
│ ┌─────────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ Quiz JSON Files │ │───▶│ │ Quiz Engine  │ │───▶│ │ PostgreSQL  │ │
│ │ - questions     │ │    │ │ - validation │ │    │ │ - answers   │ │
│ │ - scoring       │ │    │ │ - scoring    │ │    │ │ - analytics │ │
│ │ - results       │ │    │ │ - rendering  │ │    │ │ - sessions  │ │
│ └─────────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
│                     │    │                  │    │                 │
│ ┌─────────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ Card Templates  │ │    │ │ Admin Tools  │ │    │ │ File Storage│ │
│ │ - HTML/CSS      │ │    │ │ - preview    │ │    │ │ - exports   │ │
│ │ - dynamic render│ │    │ │ - analytics  │ │    │ │ - backups   │ │
│ └─────────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
└─────────────────────┘    └──────────────────┘    └─────────────────┘
```

### 2.2 결과 카드 렌더링 전략

#### 2.2.1 HTML 템플릿 기반 동적 렌더링 (채택)
```
JSON Data → Jinja2 Template → HTML Card → (Optional) Image Export
```

**장점**:
- JSON 데이터 변경 시 즉시 반영
- SEO 친화적, 텍스트 선택 가능
- 반응형 디자인 지원
- 카카오톡 공유 시 OG 태그 활용

**구현 방식**:
- 기존 card.html의 CSS 스타일을 Jinja2 템플릿으로 변환
- 결과 카드 스타일 정보를 JSON에 포함
- 필요시 Puppeteer로 HTML→이미지 변환 기능 추가

### 2.3 JSON 스키마 설계 (v2.1 - 단순화)

#### 2.3.1 Quiz Configuration Schema (실용적 버전)
```json
{
  "$schema": "https://nojam.com/schemas/quiz-v2.1.json",
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
    "scoring_method": "simple_count",  // 단순 카운팅 방식
    "randomize_questions": false,
    "show_progress": true
  },
  "questions": [
    {
      "id": "q1",
      "text": "휴대폰이 고장 났을 때 나는?",
      "type": "single_choice",
      "choices": [
        {
          "id": "q1_a",
          "text": "종이수첩 있으면 돼",
          "result_type": "ANA"  // 단순화: 하나의 결과 유형에만 1점
        },
        {
          "id": "q1_b",
          "text": "얼른 새폰 찾아봐야지",
          "result_type": "PHONE"
        },
        {
          "id": "q1_c",
          "text": "고치거나 잠시 안 써도 괜찮아",
          "result_type": "7080"
        },
        {
          "id": "q1_d",
          "text": "폰 없으면 못 살아!!",
          "result_type": "TREND"
        }
      ]
    }
  ],
  "results": {
    "7080": {
      "code": "7080",
      "title": "7080 감성형",
      "subtitle": "통기타, 쎄시봉, 낭만 감성",
      "description": "통기타, 쎄시봉, 낭만 감성의 향수와 추억을 소중히 여기는 로맨틱한 당신",
      "keywords": ["낭만", "음악", "회상"],
      "quote": "그땐 말이야, 나이트보다 통기타였지.",
      "emoji": "🎵",
      "style": {
        "gradient": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)",
        "number": "①",
        "css_class": "type-1"
      },
      "share": {
        "title": "나는 7080 감성형!",
        "description": "통기타와 낭만을 사랑하는 감성파",
        "hashtags": ["#7080감성", "#통기타", "#낭만", "#마음나이테스트"]
      }
    },
    "IMF": {
      "code": "IMF",
      "title": "IMF 생존형",
      "subtitle": "위기 속 실용주의, 절약 우선",
      "description": "위기 속 실용주의, 절약 우선 현실적이고 책임감 강한 든든한 당신",
      "keywords": ["절약", "현실", "책임감"],
      "quote": "없는 것보다 빚지는 게 무서운 거야.",
      "emoji": "💪",
      "style": {
        "gradient": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
        "number": "②",
        "css_class": "type-2"
      }
    }
    // ... 나머지 6개 결과 유형
  },
  "analytics": {
    "enabled": true,
    "events": ["quiz_started", "question_answered", "quiz_completed", "result_shared"]
  }
}
```

#### 2.3.2 주요 변경사항 (v2.0 → v2.1)
1. **점수 시스템 단순화**: `weighted_sum` → `simple_count`
2. **선택지 구조 단순화**: 복잡한 scores 객체 → 단일 result_type
3. **결과 카드 스타일 정보 추가**: CSS 클래스, 그라데이션, 이모지 등
4. **불필요한 필드 제거**: 복잡한 traits, recommendations 등 선택적으로 변경

### 2.4 디렉토리 구조 (v0.2.0)
```
nojam/
├── assets/
│   ├── quizzes/              # Quiz JSON 파일들
│   │   ├── mind-age-test.json
│   │   └── schemas/
│   │       └── quiz-v2.1.json # JSON Schema 정의
│   └── templates/
│       ├── card.html         # 결과 카드 템플릿
│       └── quiz.html         # 퀴즈 진행 템플릿
├── nojam/
│   ├── models/
│   │   ├── quiz.py          # Quiz, Question, Result Pydantic 모델
│   │   └── analytics.py     # 분석 모델
│   ├── services/
│   │   ├── quiz_engine.py   # 범용 퀴즈 엔진
│   │   ├── quiz_loader.py   # JSON 로더 & 캐시
│   │   ├── scoring.py       # 점수 계산 엔진 (simple_count 구현)
│   │   └── card_renderer.py # HTML 카드 렌더링 서비스
│   ├── admin/
│   │   ├── routes.py        # 관리자 API
│   │   ├── preview.py       # 미리보기 기능
│   │   └── validator.py     # JSON 검증
│   └── api/
│       ├── quiz_api.py      # 퀴즈 관련 API
│       └── analytics_api.py # 분석 API
```

## 3. 구현 단계별 로드맵

### 3.1 Phase 1: Core Engine (v0.2.0) - 2주
**목표**: 기본 JSON-driven 퀴즈 엔진 구현

#### 주요 작업
- [ ] **Quiz Models 설계**
  - Pydantic 모델로 단순화된 JSON 스키마 정의
  - simple_count 점수 방식 지원
  
- [ ] **Quiz Loader 구현**
  - 앱 시작 시 `/assets/quizzes/*.json` 파일 로드
  - 메모리 캐시 및 파일 변경 감지
  - JSON Schema v2.1 검증
  
- [ ] **Simple Scoring Engine**
  - simple_count 방식: 각 선택지가 특정 유형에 1점
  - 최다 득점 유형 결정 (동점 시 알파벳순)
  
- [ ] **Dynamic Card Rendering**
  - 기존 card.html을 Jinja2 템플릿으로 변환
  - JSON 데이터 기반 동적 카드 생성
  - 유형별 CSS 클래스 및 스타일 적용
  
- [ ] **기존 테스트 마이그레이션**
  - 현재 하드코딩된 "마음나이 테스트"를 JSON으로 변환
  - 기능 회귀 테스트

#### 성공 지표
- [x] 기존 테스트가 JSON 기반으로 동작
- [x] 새로운 JSON 파일 추가 시 자동으로 웹에 반영
- [x] HTML 카드가 JSON 데이터로 동적 렌더링
- [x] 모든 단위 테스트 통과

### 3.2 Phase 2: Admin Tools (v0.3.0) - 1주  
**목표**: 내부 팀을 위한 관리 도구

#### 주요 작업
- [ ] **Quiz Preview System**
  - `/admin/preview/{quiz_id}` - 배포 전 미리보기
  - 실시간 JSON 편집 및 즉시 반영
  
- [ ] **JSON Validator**
  - 웹 기반 JSON 스키마 검증 도구
  - 오류 위치 및 수정 제안
  
- [ ] **Card Image Export**
  - Puppeteer 기반 HTML→이미지 변환
  - 카카오톡 공유용 이미지 자동 생성
  
- [ ] **Analytics Dashboard**
  - 테스트별 완료율, 결과 분포, 공유율 차트
  - 실시간 사용자 현황

#### 성공 지표
- [x] 비개발자도 JSON 파일 수정 가능
- [x] 실시간 분석 데이터 확인
- [x] 카드 이미지 자동 생성

### 3.3 Phase 3: Advanced Features (v0.4.0) - 2주
**목표**: 고급 기능 및 최적화

#### 주요 작업
- [ ] **Advanced Scoring Methods**
  - weighted_sum, percentage 등 다양한 점수 방식 지원
  - 기존 simple_count와 호환성 유지
  
- [ ] **Advanced Question Types**
  - 슬라이더형 질문 (1-10 점수)
  - 이미지 선택형 질문
  - 순위 매기기 질문
  
- [ ] **Multi-language Support**
  - i18n 프레임워크 도입
  - 언어별 JSON 파일 관리
  
- [ ] **Performance Optimization**
  - Redis 캐시 도입
  - 카드 이미지 CDN 연동
  - DB 쿼리 최적화

#### 성공 지표
- [x] 다양한 점수 방식 지원
- [x] 다양한 질문 형식 활용
- [x] 페이지 로딩 시간 < 2초

## 4. 기술적 고려사항

### 4.1 카드 렌더링 최적화
- **템플릿 캐싱**: Jinja2 템플릿 컴파일 결과 캐시
- **이미지 생성 최적화**: Puppeteer 인스턴스 재사용, 병렬 처리
- **CDN 활용**: 생성된 카드 이미지는 CDN에 캐시

### 4.2 확장성 설계
- **점수 방식 확장**: simple_count 외 다양한 방식 플러그인 구조
- **템플릿 확장**: 카드 외 다양한 결과 표시 방식 지원
- **API 버전 관리**: v2.1, v2.2 등 스키마 버전 동시 지원

### 4.3 보안 고려사항
- **JSON 검증**: 악의적인 JSON 파일 업로드 방지
- **템플릿 보안**: Jinja2 autoescape 활성화
- **이미지 생성 제한**: Puppeteer 리소스 사용량 제한

## 5. 예상 효과 및 KPI

### 5.1 개발 효율성
- **테스트 제작 시간**: 2일 → 2시간 (90% 단축)
- **카드 디자인 시간**: 1일 → 10분 (JSON 수정만으로 완료)
- **배포 주기**: 주 1회 → 일 1회

### 5.2 비즈니스 임팩트
- **테스트 다양성**: 월 1개 → 월 5개 신규 테스트
- **사용자 참여도**: 카드 공유율 30% 증가
- **수익성**: 다양한 테스트를 통한 광고 수익 증대

---

**문서 변경 이력**
| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| 2.0 | 2025-01-21 | o3-assistant | 내부 테스트 제작용 플랫폼 로드맵 고도화 |
| 2.1 | 2025-01-21 | o3-assistant | 실제 샘플 테스트 분석 반영, 스키마 단순화, 카드 렌더링 방식 결정 | 