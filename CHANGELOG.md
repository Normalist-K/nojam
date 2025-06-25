# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-21

### Added - Phase 1: JSON-Driven Platform
- **Quiz Models (Pydantic v2)**: JSON Schema v2.1 기반 완전한 데이터 모델
  - `nojam/models/quiz.py`: Quiz, QuizMeta, Question, Choice, Result 등
  - 강력한 데이터 검증 (문항-선택지 일치성, 결과 유형 정합성)
  - IDE 자동완성 지원
- **Quiz Loader**: JSON 파일 동적 로딩 및 캐시 관리
  - `nojam/services/loader.py`: 파일 변경 감지, 메모리 캐시, 싱글턴 패턴
  - 실시간 퀴즈 로딩 (서버 재시작 불필요)
- **Scoring Engine**: 확장 가능한 점수 계산 시스템
  - `nojam/services/scoring.py`: Simple Count 방식 구현
  - 점수 분포 계산, 동점 시 알파벳순 결정
  - Weighted Sum, Percentage 방식 확장 준비
- **Dynamic Templates**: JSON 기반 동적 퀴즈 렌더링
  - 가변 문항 수 지원 (현재 15문항)
  - 동적 결과 카드 생성 (TailwindCSS 그라데이션)
  - 하위 호환성 유지 (기존 10문항 지원)
- **새로운 API 엔드포인트**:
  - `GET /api/quizzes`: 사용 가능한 퀴즈 목록
  - `GET /api/quiz/{quiz_id}`: 특정 퀴즈 상세 정보
  - `GET /quiz?quiz_id=xxx`: 동적 퀴즈 선택 지원

### Added - JSON Quiz System
- **완성된 샘플 퀴즈**: `assets/quizzes/mind-age-test.json`
  - 15문항, 8결과 유형 (7080, IMF, ACT, MBC, PHONE, ANA, TREND, JUNK)
  - 결과별 스타일 정보 (그라데이션, 이모지, 키워드)
- **JSON Schema**: `assets/schemas/quiz-schema-v2.1.json`
  - 구조 검증, IDE 자동완성 지원
- **디렉토리 구조**: `assets/quizzes/`, `assets/schemas/`, `assets/templates/`

### Changed - Pydantic v2 Migration
- **모든 Pydantic 모델 v2 업그레이드**:
  - `@validator` → `@field_validator`
  - `Config` 클래스 → `model_config = ConfigDict(...)`
  - `.dict()` → `.model_dump()`
  - `parse_obj()` → `model_validate()`
- **타입 힌트 현대화**: `Optional[X]` → `X | None`, `List` → `list`, `Dict` → `dict`
- **린트 설정 개선**: `ruff.toml` → `pyproject.toml` 통합

### Enhanced
- **하위 호환성**: 기존 하드코딩 로직과 완벽 호환
  - JSON 시스템 실패 시 자동 폴백
  - 기존 답변 형식 지원 (A, B, C, D)
  - 기존 API 엔드포인트 유지
- **성능 최적화**: 퀴즈 파일 캐싱, 파일 변경 감지
- **확장성**: 새로운 퀴즈 추가가 JSON 파일 생성만으로 가능

### Fixed
- 모든 린트 오류 수정 (74개 → 0개)
- Pydantic v2 호환성 문제 해결
- 타입 안정성 향상

### Documentation
- **API 명세서 v0.2.0**: Phase 1 구현 내용 반영
- **DB 스키마 v0.2.0**: 동적 퀴즈 지원 내용 추가
- **Phase 1 완료 보고서**: 구현 성과 및 다음 단계 정리

### Technical Details
- **테스트 커버리지**: 7/7 단위 테스트 통과
- **코드 품질**: 모든 린트 검사 통과
- **타입 안정성**: Pydantic v2 강력한 검증
- **메모리 효율성**: 싱글턴 패턴, 캐싱 시스템

## [0.1.0] - 2025-01-21

### Added
- 프로젝트 기본 구조 (services/db/web/external 패키지)
- FastAPI 기반 웹 애플리케이션 스켈레톤
- aiosqlite 기반 AnswerRepository (비동기 CRUD)
- 심리테스트 결과 계산 서비스 (quiz.py)
- Kakao 카카오톡 공유 Stub 모듈
- Google AdSense 광고 Stub 모듈
- TailwindCSS 기반 반응형 웹 템플릿
  - 퀴즈 페이지 (10문항 폼)
  - 결과 페이지 (카드 이미지 슬롯, 광고 영역)
- structlog 기반 JSON 로깅 시스템
- GA4 이벤트 및 광고 지표 로깅 헬퍼
- GitHub Actions CI/CD 파이프라인
- Docker 컨테이너 배포 설정 (Render.com)
- 단위 테스트 7개 (모든 주요 모듈 커버)
  - Repository CRUD 테스트
  - Quiz 서비스 로직 테스트
  - 외부 SDK Stub 테스트
  - 로깅 헬퍼 테스트
  - 웹 라우트 통합 테스트

### Technical Details
- Python 3.11 + uv 패키지 관리
- FastAPI + Jinja2 + HTMX 스택
- SQLite → Supabase 마이그레이션 준비
- TDD 개발 방식 (Red-Green-Refactor)
- SOLID 원칙 및 Clean Architecture 적용
- Conventional Commits 규칙 준수

### Deferred (TODO)
- E2E 테스트 (Playwright 비동기 루프 충돌 해결 필요)
- 실제 Kakao SDK 연동
- 실제 Google AdSense 연동
- Supabase 데이터베이스 마이그레이션

### Known Issues
- E2E 테스트에서 FastAPI TestClient와 Playwright 이벤트 루프 충돌
- 현재는 Stub 모듈로만 외부 서비스 연동 (실제 SDK 미적용)

---

## [Unreleased]

### Planned for v0.3.0 (Phase 2: Admin Tools)
- Preview System: 퀴즈 미리보기 및 테스트 도구
- JSON Validator: 웹 기반 JSON 검증 인터페이스  
- Analytics Dashboard: 실시간 통계 대시보드
- A/B Testing: 퀴즈 버전 비교 테스트

### Planned for v0.4.0 (Phase 3: Advanced Features)
- Multi-language: 다국어 지원 시스템
- Advanced Question Types: slider, ranking, multiple_choice
- AI Result Generation: GPT 기반 동적 결과 생성
- Performance Optimization: 캐시 최적화, CDN 연동 