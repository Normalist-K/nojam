# JSON-Driven 심리테스트 플랫폼 로드맵 v2.0

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
│ │ Asset Library   │ │    │ │ Admin Tools  │ │    │ │ File Storage│ │
│ │ - card images   │ │    │ │ - preview    │ │    │ │ - images    │ │
│ │ - icons         │ │    │ │ - analytics  │ │    │ │ - exports   │ │
│ └─────────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
└─────────────────────┘    └──────────────────┘    └─────────────────┘
```

### 2.2 JSON 스키마 설계

#### 2.2.1 Quiz Configuration Schema
```json
{
  "$schema": "https://nojam.com/schemas/quiz-v2.json",
  "meta": {
    "id": "mind_age_v1",
    "version": "1.0.0",
    "title": "🕰️ 나는 어떤 시대형 인간일까?",
    "description": "베이비붐 세대를 위한 심리테스트",
    "author": "nojam-team",
    "created_at": "2025-01-21",
    "tags": ["psychology", "generation", "baby-boomer"],
    "estimated_time": "3-5분",
    "target_age": "50-70",
    "language": "ko"
  },
  "config": {
    "question_count": 10,
    "result_types": 8,
    "scoring_method": "weighted_sum",
    "randomize_questions": false,
    "randomize_choices": false,
    "allow_skip": false,
    "show_progress": true,
    "analytics_enabled": true
  },
  "branding": {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2",
    "logo_url": "/assets/logos/mind-age.svg",
    "og_image": "/assets/og/mind-age-og.jpg",
    "favicon": "/assets/favicons/mind-age.ico"
  },
  "questions": [
    {
      "id": "q1",
      "type": "single_choice",
      "category": "technology",
      "text": "휴대폰이 고장 났을 때 나는?",
      "instruction": "가장 가까운 반응을 선택해주세요",
      "required": true,
      "choices": [
        {
          "id": "q1_a",
          "text": "종이수첩 있으면 돼",
          "emoji": "📝",
          "scores": {
            "ANA": 1,
            "7080": 0.5
          }
        },
        {
          "id": "q1_b", 
          "text": "얼른 새폰 찾아봐야지",
          "emoji": "📱",
          "scores": {
            "PHONE": 1,
            "TREND": 0.3
          }
        },
        {
          "id": "q1_c",
          "text": "고치거나 잠시 안 써도 괜찮아",
          "emoji": "🔧",
          "scores": {
            "7080": 1,
            "IMF": 0.4
          }
        },
        {
          "id": "q1_d",
          "text": "폰 없으면 못 살아!!",
          "emoji": "😱",
          "scores": {
            "TREND": 1,
            "PHONE": 0.6
          }
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
      "detailed_description": "당신은 70-80년대의 낭만적인 감성을 간직한 분입니다. 통기타 선율과 쎄시봉의 추억, 그 시절의 순수했던 사랑 이야기들을 그리워하며...",
      "keywords": ["낭만", "음악", "회상", "추억", "감성"],
      "quote": "그땐 말이야, 나이트보다 통기타였지.",
      "percentage_range": [12, 18],
      "traits": [
        {
          "name": "감수성",
          "score": 95,
          "description": "예술과 음악에 대한 깊은 감수성"
        },
        {
          "name": "향수",
          "score": 90,
          "description": "과거에 대한 강한 그리움"
        },
        {
          "name": "낭만성",
          "score": 85,
          "description": "로맨틱한 상황을 선호"
        }
      ],
      "recommendations": [
        "통기타 배우기",
        "7080 음악 감상",
        "추억의 장소 방문",
        "일기 쓰기"
      ],
      "compatible_types": ["DRM", "JUNK"],
      "image": {
        "card_url": "/assets/cards/7080-card.jpg",
        "background_url": "/assets/backgrounds/7080-bg.jpg",
        "icon_url": "/assets/icons/7080-icon.svg"
      },
      "share": {
        "title": "나는 7080 감성형!",
        "description": "통기타와 낭만을 사랑하는 감성파",
        "hashtags": ["#7080감성", "#통기타", "#낭만", "#마음나이테스트"]
      }
    }
  },
  "analytics": {
    "events": [
      {
        "name": "quiz_started",
        "properties": ["quiz_id", "user_agent", "referrer"]
      },
      {
        "name": "question_answered", 
        "properties": ["quiz_id", "question_id", "choice_id", "time_spent"]
      },
      {
        "name": "quiz_completed",
        "properties": ["quiz_id", "result_type", "total_time", "completion_rate"]
      },
      {
        "name": "result_shared",
        "properties": ["quiz_id", "result_type", "share_platform"]
      }
    ],
    "goals": [
      {
        "name": "completion_rate",
        "target": 0.75,
        "description": "75% 이상의 사용자가 테스트를 완료"
      },
      {
        "name": "share_rate", 
        "target": 0.30,
        "description": "30% 이상의 사용자가 결과를 공유"
      }
    ]
  }
}
```

### 2.3 디렉토리 구조 (v0.2.0)
```
nojam/
├── assets/
│   ├── quizzes/              # Quiz JSON 파일들
│   │   ├── mind-age-v1.json
│   │   ├── personality-v2.json
│   │   └── career-fit-v1.json
│   ├── images/
│   │   ├── cards/            # 결과 카드 이미지
│   │   ├── backgrounds/      # 배경 이미지
│   │   ├── icons/           # 아이콘
│   │   └── og/              # OG 이미지
│   └── schemas/
│       └── quiz-v2.json     # JSON Schema 정의
├── nojam/
│   ├── models/
│   │   ├── quiz.py          # Quiz, Question, Result Pydantic 모델
│   │   └── analytics.py     # 분석 모델
│   ├── services/
│   │   ├── quiz_engine.py   # 범용 퀴즈 엔진
│   │   ├── quiz_loader.py   # JSON 로더 & 캐시
│   │   ├── scoring.py       # 점수 계산 엔진
│   │   └── analytics.py     # 분석 서비스
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
  - Pydantic 모델로 JSON 스키마 정의
  - 타입 안전성 및 검증 로직 구현
  
- [ ] **Quiz Loader 구현**
  - 앱 시작 시 `/assets/quizzes/*.json` 파일 로드
  - 메모리 캐시 및 파일 변경 감지
  - JSON Schema 검증
  
- [ ] **범용 Scoring Engine**
  - weighted_sum, max_score, percentage 등 다양한 채점 방식
  - 동점 처리 로직 (알파벳순, 최근 답변 우선 등)
  
- [ ] **Dynamic Template Rendering**
  - Jinja2 템플릿에서 JSON 데이터 동적 렌더링
  - 반응형 UI 컴포넌트 라이브러리
  
- [ ] **기존 테스트 마이그레이션**
  - 현재 하드코딩된 "마음나이 테스트"를 JSON으로 변환
  - 기능 회귀 테스트

#### 성공 지표
- [x] 기존 테스트가 JSON 기반으로 동작
- [x] 새로운 JSON 파일 추가 시 자동으로 웹에 반영
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
  
- [ ] **Analytics Dashboard**
  - 테스트별 완료율, 결과 분포, 공유율 차트
  - 실시간 사용자 현황
  
- [ ] **A/B Testing Framework**
  - 동일 테스트의 여러 버전 동시 운영
  - 트래픽 분할 및 성과 비교

#### 성공 지표
- [x] 비개발자도 JSON 파일 수정 가능
- [x] 실시간 분석 데이터 확인
- [x] A/B 테스트 설정 및 결과 분석

### 3.3 Phase 3: Advanced Features (v0.4.0) - 2주
**목표**: 고급 기능 및 최적화

#### 주요 작업
- [ ] **Multi-language Support**
  - i18n 프레임워크 도입
  - 언어별 JSON 파일 관리
  
- [ ] **Advanced Question Types**
  - 슬라이더형 질문 (1-10 점수)
  - 이미지 선택형 질문
  - 순위 매기기 질문
  
- [ ] **Dynamic Result Generation**
  - AI 기반 개인화된 결과 설명
  - 사용자 답변 패턴 분석
  
- [ ] **Performance Optimization**
  - Redis 캐시 도입
  - CDN 연동 (이미지, 정적 파일)
  - DB 쿼리 최적화
  
- [ ] **Advanced Analytics**
  - 사용자 여정 분석
  - 이탈 지점 분석
  - 코호트 분석

#### 성공 지표
- [x] 다국어 테스트 지원
- [x] 다양한 질문 형식 활용
- [x] 페이지 로딩 시간 < 2초

## 4. 기술적 고려사항

### 4.1 성능 최적화
- **메모리 캐시**: Quiz JSON은 앱 시작 시 로드하여 메모리에 캐시
- **이미지 최적화**: WebP 포맷 사용, 반응형 이미지 제공
- **CDN 활용**: 정적 자원은 Cloudflare Images 활용
- **DB 최적화**: 인덱스 설계, 쿼리 최적화

### 4.2 확장성 설계
- **수평 확장**: Stateless 앱 서버, 외부 캐시 사용
- **마이크로서비스 준비**: 퀴즈 엔진과 분석 서비스 분리 가능한 구조
- **API 버전 관리**: v1, v2 API 동시 지원

### 4.3 보안 고려사항
- **JSON 검증**: 악의적인 JSON 파일 업로드 방지
- **XSS 방지**: 사용자 입력 및 JSON 콘텐츠 sanitization
- **Rate Limiting**: API 호출 제한
- **CSRF 보호**: 폼 제출 시 CSRF 토큰 검증

## 5. 운영 및 모니터링

### 5.1 배포 전략
- **Blue-Green 배포**: 무중단 배포
- **Feature Flag**: 새로운 기능의 점진적 롤아웃
- **Rollback 계획**: 문제 발생 시 즉시 이전 버전으로 복구

### 5.2 모니터링
- **실시간 알림**: 오류율, 응답시간 임계값 초과 시 Slack 알림
- **사용자 분석**: GA4 + 자체 분석 시스템
- **성능 모니터링**: APM 도구 도입 (New Relic, DataDog)

### 5.3 백업 및 복구
- **데이터 백업**: 일일 자동 백업, 주간 백업 검증
- **재해 복구**: RTO 4시간, RPO 1시간 목표
- **버전 관리**: Quiz JSON 파일의 Git 기반 버전 관리

## 6. 예상 효과 및 KPI

### 6.1 개발 효율성
- **테스트 제작 시간**: 2일 → 2시간 (90% 단축)
- **배포 주기**: 주 1회 → 일 1회
- **버그 발생률**: JSON 검증을 통한 50% 감소

### 6.2 비즈니스 임팩트
- **테스트 다양성**: 월 1개 → 월 5개 신규 테스트
- **사용자 참여도**: 재방문율 30% 증가
- **수익성**: 다양한 테스트를 통한 광고 수익 증대

### 6.3 측정 지표
- **기술 지표**: 응답시간, 에러율, 캐시 히트율
- **사용자 지표**: 완료율, 공유율, 재방문율  
- **비즈니스 지표**: 신규 테스트 제작 속도, 광고 수익

---

## 7. 위험 요소 및 대응 방안

### 7.1 기술적 위험
- **JSON 스키마 변경**: 하위 호환성 유지, 마이그레이션 도구 제공
- **성능 저하**: 부하 테스트, 성능 모니터링 강화
- **보안 취약점**: 정기적인 보안 감사, 침투 테스트

### 7.2 운영 위험  
- **콘텐츠 품질**: JSON 검증 도구, 미리보기 시스템
- **사용자 혼란**: 일관된 UI/UX, 사용자 테스트
- **데이터 손실**: 백업 시스템, 복구 절차 문서화

---

**문서 변경 이력**
| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| 2.0 | 2025-01-21 | o3-assistant | 내부 테스트 제작용 플랫폼 로드맵 고도화 | 