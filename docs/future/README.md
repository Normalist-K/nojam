# 🚀 Future Plans (향후 계획)

이 폴더는 v0.2.0 이후 구현 예정인 기능들과 계획 문서들입니다.

## 📋 포함된 문서들

### 🗺️ json_driven_platform_roadmap.md
- **JSON-driven 심리테스트 플랫폼 로드맵 v2.0**
- 3단계 구현 계획 (Core Engine → Admin Tools → Advanced Features)
- 상세한 JSON 스키마 설계
- 기술적 고려사항 및 KPI

### 🧪 e2e_todo.md
- **E2E 테스트 환경 개선 계획**
- Playwright 비동기 루프 충돌 해결 방안
- 별도 프로세스 전략 vs httpx + HTML 파싱
- v0.2.0 목표 및 테스트 시나리오

### 💰 ads_integration.md
- **실제 광고 SDK 연동 가이드**
- Google AdSense, Kakao AdFit 승인 절차
- Stub → 실제 SDK 전환 계획
- 로그 파이프라인 및 운영 주의사항

### 📊 log_todos.md
- **고급 로깅 시스템 TODO**
- structlog 최적화, GA4 배치 처리
- 외부 모니터링 도구 연동
- 성능 최적화 및 샘플링

## 🎯 우선순위

### Phase 1: v0.2.0 (2주)
1. **JSON-driven Core Engine** 🥇
   - Quiz Models, Loader, Scoring Engine
   - 기존 테스트 JSON 마이그레이션

### Phase 2: v0.3.0 (1주)  
2. **Admin Tools** 🥈
   - Preview System, JSON Validator
   - Analytics Dashboard

### Phase 3: v0.4.0 (2주)
3. **Advanced Features** 🥉
   - Multi-language, Advanced Question Types
   - Performance Optimization

### 추후 검토
4. **E2E 테스트 환경** ⏳
5. **실제 광고 연동** ⏳
6. **고급 로깅 시스템** ⏳

## 📝 문서 상태

- ✅ **완성**: json_driven_platform_roadmap.md
- 🔄 **검토 중**: e2e_todo.md, ads_integration.md  
- 📝 **초안**: log_todos.md

---

💡 **Tip**: 구현 시작 전에 해당 문서를 `active/` 폴더로 이동하고, 완료 후에는 `archived/` 폴더로 이동하여 정리하세요. 