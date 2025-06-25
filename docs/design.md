# 프로젝트 설계서 (최종 목표)

## 1. 프로젝트 비전
베이비붐 세대(50-66세)를 대상으로 한 **JSON-driven 심리테스트 플랫폼**을 구축하여, 내부 팀이 코드 수정 없이 다양한 심리테스트를 1시간 내에 제작·배포할 수 있는 시스템을 만든다.

### 핵심 목표
- 🎯 **사용자 경험**: 직관적이고 재미있는 심리테스트 경험
- ⚡ **제작 효율성**: JSON 파일만으로 새로운 테스트 제작 (2일 → 2시간)
- 📈 **확장성**: 월 1개 → 월 5개 신규 테스트 배포
- 💰 **수익성**: 카카오톡 공유 + 광고 수익 모델

## 2. 개발 원칙
- **TDD (Test-Driven Development)**: `Red → Green → Refactor`
- **SOLID 원칙**: 단일 책임, 개방-폐쇄, 리스코프 치환, 인터페이스 분리, 의존 역전
- **Clean Architecture**: 도메인 중심, 의존성 역전
- **Conventional Commits**: 일관된 커밋 메시지 규칙

## 3. 기술 스택 & 아키텍처

### 3.1 핵심 기술
```
Frontend: HTMX + TailwindCSS + Jinja2
Backend:  FastAPI + Python 3.11
Database: SQLite → Supabase (PostgreSQL)
Testing:  pytest + Playwright
Deploy:   Docker + Render.com
Package:  uv (Python package manager)
```

### 3.2 시스템 아키텍처
```
[사용자] ↔ [Web UI] ↔ [API] ↔ [Service] ↔ [Repository] ↔ [Database]
                                    ↓
                              [External APIs]
                            (Kakao, AdSense, GA4)
```

### 3.3 프로젝트 구조
```
nojam/
├── nojam/                    # 메인 패키지
│   ├── services/            # 비즈니스 로직
│   ├── db/                  # 데이터 액세스
│   ├── web/                 # 웹 계층 (라우트, 템플릿)
│   ├── external/            # 외부 API 연동
│   └── main.py             # FastAPI 앱
├── tests/                   # 테스트 코드
├── docs/                    # 문서화
└── pyproject.toml          # 의존성 관리
```

## 4. 발전 단계

### Phase 0: v0.1.0 ✅ **완료**
- 기본 프로젝트 구조 및 FastAPI 앱
- SQLite 기반 데이터베이스 (aiosqlite)
- 하드코딩된 심리테스트 로직 (10문항 → 8가지 결과)
- 기본 웹 UI (TailwindCSS)
- 외부 API Stub (Kakao, AdSense)
- CI/CD 파이프라인 (GitHub Actions)
- 단위 테스트 (7개)

### Phase 1: v0.2.0 🎯 **JSON-driven Core Engine**
- **Quiz Models**: 동적 테스트 구조 정의
- **JSON Loader**: 파일 기반 테스트 로딩
- **Scoring Engine**: 유연한 점수 계산 시스템
- **Dynamic Templates**: JSON 기반 UI 렌더링
- 기존 하드코딩 테스트 → JSON 마이그레이션

### Phase 2: v0.3.0 🔧 **Admin Tools**
- **Preview System**: 배포 전 테스트 미리보기
- **JSON Validator**: 스키마 검증 도구
- **Analytics Dashboard**: 테스트별 통계
- **A/B Testing**: 결과 비교 시스템

### Phase 3: v0.4.0 🚀 **Advanced Features**
- **Multi-language**: 다국어 지원
- **Advanced Question Types**: 이미지, 슬라이더 등
- **AI Result Generation**: 자동 결과 생성
- **Performance Optimization**: 캐싱, CDN 등

### Phase 4: v1.0.0 🌟 **Production Ready**
- **Real SDK Integration**: 실제 광고 연동
- **Advanced Logging**: 외부 모니터링 연동
- **E2E Testing**: 완전한 테스트 환경
- **Supabase Migration**: PostgreSQL 전환

## 5. 데이터 모델

### 5.1 현재 (v0.1.0)
```sql
-- 단일 테스트 결과 저장
CREATE TABLE answers (
  id TEXT PRIMARY KEY,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  answers_json TEXT NOT NULL,
  result_type TEXT CHECK(...),
  ua_hash CHAR(64)
);
```

### 5.2 목표 (v0.2.0+)
```sql
-- 다중 테스트 지원
CREATE TABLE quizzes (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  config_json TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_results (
  id TEXT PRIMARY KEY,
  quiz_id TEXT REFERENCES quizzes(id),
  answers_json TEXT NOT NULL,
  result_data_json TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 6. JSON 스키마 (목표)

### 6.1 테스트 정의
```json
{
  "metadata": {
    "id": "mind-age-test",
    "title": "마음나이 테스트",
    "description": "당신의 진짜 마음나이는?",
    "version": "1.0.0"
  },
  "config": {
    "question_count": 10,
    "result_types": 8,
    "scoring_method": "weighted_sum"
  },
  "questions": [...],
  "results": [...],
  "branding": {
    "primary_color": "#3B82F6",
    "logo_url": "/static/logo.png"
  }
}
```

### 6.2 결과 정의
```json
{
  "results": [
    {
      "id": "7080",
      "title": "7080 세대",
      "description": "향수와 낭만을 아는 당신",
      "traits": [
        {"name": "향수", "score": 85},
        {"name": "낭만", "score": 90}
      ],
      "image_url": "/static/results/7080.webp",
      "share_text": "나는 7080 세대! 당신은?"
    }
  ]
}
```

## 7. 품질 보증

### 7.1 테스트 전략
- **단위 테스트**: Service 로직, Repository CRUD
- **통합 테스트**: API 엔드포인트
- **E2E 테스트**: 전체 사용자 플로우
- **목표 커버리지**: 단위 70%+, E2E 50%+

### 7.2 코드 품질
- **ruff**: 린터 + 포매터
- **mypy**: 정적 타입 검사
- **pre-commit**: 커밋 전 품질 검사

## 8. 운영 & 모니터링

### 8.1 로깅
- **structlog**: 구조화된 JSON 로그
- **GA4**: 사용자 행동 분석
- **광고 지표**: RPM, CTR 추적

### 8.2 배포
- **Docker**: 컨테이너화
- **Render.com**: 클라우드 배포
- **GitHub Actions**: CI/CD 자동화

### 8.3 확장성
- **Stateless App**: 수평 확장 가능
- **CDN**: 정적 자원 최적화
- **Database Sharding**: 대용량 트래픽 대응

## 9. 비즈니스 모델
- **무료 서비스**: 심리테스트 이용
- **광고 수익**: Google AdSense, Kakao AdFit
- **바이럴 마케팅**: 카카오톡 공유 기능
- **프리미엄**: 상세 분석 리포트 (향후)

## 10. 성공 지표 (KPI)
- **제작 효율성**: 테스트 제작 시간 90% 단축
- **콘텐츠 다양성**: 월 신규 테스트 5배 증가
- **사용자 참여**: 공유율 30% 이상
- **기술 품질**: 테스트 커버리지 70% 이상

---

💡 **참고**: 구체적인 구현 세부사항은 `docs/active/`, `docs/future/` 폴더의 문서들을 참조하세요.

**문서 변경 이력**
| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| 1.0 | 2025-06-21 | o3-assistant | 최초 작성 (v0.1.0 기준) |
| 2.0 | 2025-06-21 | o3-assistant | 전체 프로젝트 목표 설계서로 재작성 | 