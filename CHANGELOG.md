# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

### Planned for v0.2.0
- JSON-driven 심리테스트 플랫폼 구현
- E2E 테스트 환경 개선 (별도 프로세스 전략)
- 실제 심리테스트 콘텐츠 적용 (sample_test.md 기반)
- 결과 카드 이미지 시스템 구현 