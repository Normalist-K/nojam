# 📋 Phase 2 구현 체크리스트 (v0.3.0) - 세분화 버전

이 문서는 Phase 2에서 구현해야 할 기능들을 **커서로 한 번에 구현 가능한 단위**로 세분화한 체크리스트입니다.  
**목표**: 공유 기능, 광고 연동, 사용자 통계 기능 구현

## 🎯 Phase 2 핵심 목표

### 비즈니스 목표
- **사용자 참여도 증대**: 카카오톡/네이버밴드 공유를 통한 바이럴 확산
- **수익화 기반 구축**: Google AdSense, Kakao AdFit 광고 연동
- **데이터 기반 의사결정**: GA4 통계 및 실시간 대시보드 구축

### 기술적 목표
- **SNS 공유 최적화**: OG 태그, 이미지 생성, 딥링크 지원
- **광고 SDK 통합**: Stub → 실제 SDK 전환, 성과 측정
- **분석 시스템**: 사용자 행동 추적, 실시간 통계 API

---

## 🔗 1. 결과 공유하기 기능

### 1.1 카카오톡 공유 - 기본 구조 설정 (1시간)
- [ ] **환경 설정 및 Stub 제거**
  - [ ] `KAKAO_JAVASCRIPT_KEY` 환경변수 추가 (settings.py)
  - [ ] `external/kakao_stub.py` 파일 제거
  - [ ] 실제 Kakao SDK 스크립트 추가 (base.html)
  
**커밋 메시지**: `feat: setup Kakao SDK integration and remove stub implementation`

### 1.2 카카오톡 공유 - 핵심 JavaScript 구현 (1.5시간)
- [ ] **JavaScript 공유 로직 구현**
  - [ ] `static/js/kakao-share.js` 파일 생성
  - [ ] Kakao.Share.sendDefault() 기본 구현
  - [ ] 공유 버튼 이벤트 리스너 추가
  
**커밋 메시지**: `feat: implement Kakao share JavaScript functionality`

### 1.3 카카오톡 공유 - 동적 콘텐츠 생성 (2시간)
- [ ] **공유 콘텐츠 동적 생성**
  - [ ] 결과별 공유 메시지 템플릿 구현
  - [ ] 딥링크 생성 로직 추가 (`/quiz?utm_source=kakao`)
  - [ ] OG 태그 동적 생성 (result.html)
  
**커밋 메시지**: `feat: add dynamic content generation for Kakao sharing`

### 1.4 카카오톡 공유 - 이벤트 로깅 (1시간)
- [ ] **공유 이벤트 추적**
  - [ ] 공유 성공/실패 이벤트 로깅 구현
  - [ ] GA4 이벤트 전송 로직 추가
  - [ ] 공유 클릭률 통계 수집
  
**커밋 메시지**: `feat: add event tracking for Kakao share interactions`

### 1.5 네이버 밴드 공유 - 기본 모듈 생성 (1시간)
- [ ] **밴드 공유 모듈 기본 구조**
  - [ ] `external/band_integration.py` 모듈 생성
  - [ ] 네이버 밴드 공유 URL 스키마 구현
  - [ ] 기본 공유 함수 템플릿 작성
  
**커밋 메시지**: `feat: create Naver Band integration module with basic structure`

### 1.6 네이버 밴드 공유 - UI 통합 (1.5시간)
- [ ] **밴드 공유 버튼 추가**
  - [ ] result.html에 밴드 공유 버튼 UI 추가
  - [ ] 모바일/데스크톱 반응형 디자인 적용
  - [ ] 공유 버튼 스타일링 (TailwindCSS)
  
**커밋 메시지**: `feat: add Naver Band share button UI with responsive design`

### 1.7 공유 기능 - 메타데이터 최적화 (1시간)
- [ ] **OG 태그 완성**
  - [ ] 결과별 개별 title, description 생성
  - [ ] 공유 이미지 URL 동적 생성
  - [ ] Twitter Card 메타데이터 추가
  
**커밋 메시지**: `feat: optimize social media metadata for better sharing`

---

## 💰 2. 광고 붙이기 기능

### 2.1 Google AdSense - 환경 설정 (30분)
- [ ] **AdSense 환경변수 설정**
  - [ ] `GOOGLE_ADSENSE_CLIENT_ID` 환경변수 추가
  - [ ] settings.py에 AdSense 설정 추가
  - [ ] 개발/프로덕션 환경 분기 로직
  
**커밋 메시지**: `feat: add Google AdSense environment configuration`

### 2.2 Google AdSense - Stub 제거 및 실제 코드 통합 (1시간)
- [ ] **AdSense 실제 SDK 전환**
  - [ ] `external/adsense_stub.py` 제거
  - [ ] `external/adsense_integration.py` 생성
  - [ ] 실제 AdSense 스크립트 코드 추가
  
**커밋 메시지**: `feat: replace AdSense stub with real SDK integration`

### 2.3 Google AdSense - 광고 슬롯 구현 (1.5시간)
- [ ] **result.html 광고 슬롯 추가**
  - [ ] 광고 슬롯 div 추가 및 스타일링
  - [ ] CLS 방지를 위한 고정 높이 설정
  - [ ] 모바일 반응형 광고 구현
  
**커밋 메시지**: `feat: implement AdSense ad slots with CLS optimization`

### 2.4 Kakao AdFit - 기본 설정 (1시간)
- [ ] **AdFit 환경 설정**
  - [ ] `KAKAO_ADFIT_CLIENT_ID` 환경변수 추가
  - [ ] `external/adfit_integration.py` 모듈 생성
  - [ ] AdFit SDK 스크립트 추가
  
**커밋 메시지**: `feat: setup Kakao AdFit integration environment`

### 2.5 A/B 테스트 - 광고 로테이션 구현 (2시간)
- [ ] **광고 A/B 테스트 로직**
  - [ ] AdSense/AdFit 50:50 분배 로직 구현
  - [ ] 사용자 세션 기반 일관성 유지
  - [ ] A/B 테스트 결과 로깅
  
**커밋 메시지**: `feat: implement A/B testing for AdSense vs AdFit`

### 2.6 광고 성과 측정 - 기본 로깅 (1시간)
- [ ] **광고 지표 수집**
  - [ ] impression, click 이벤트 로깅
  - [ ] 광고 위치별 성과 추적
  - [ ] 기본 CTR 계산 로직
  
**커밋 메시지**: `feat: add basic ad performance tracking and logging`

---

## 📈 3. 사용자 통계 기능

### 3.1 Google Analytics 4 - 기본 설정 (1시간)
- [ ] **GA4 환경 설정**
  - [ ] `GA4_MEASUREMENT_ID` 환경변수 추가
  - [ ] gtag.js 스크립트 추가 (base.html)
  - [ ] 기본 페이지뷰 추적 활성화
  
**커밋 메시지**: `feat: setup Google Analytics 4 basic configuration`

### 3.2 GA4 - 커스텀 이벤트 구현 (1.5시간)
- [ ] **맞춤 이벤트 추가**
  - [ ] quiz_start, quiz_complete, result_view 이벤트
  - [ ] JavaScript 이벤트 추적 함수 생성
  - [ ] 서버사이드 이벤트 로깅 추가
  
**커밋 메시지**: `feat: implement custom GA4 events for quiz interactions`

### 3.3 통계 API - 기본 구조 (1시간)
- [ ] **통계 API 모듈 생성**
  - [ ] `nojam/api/` 폴더 생성
  - [ ] `stats.py` 라우터 파일 생성
  - [ ] 기본 API 엔드포인트 구조 설정
  
**커밋 메시지**: `feat: create statistics API module structure`

### 3.4 실시간 통계 API - 구현 (2시간)
- [ ] **실시간 통계 엔드포인트**
  - [ ] `/api/stats/realtime` 구현
  - [ ] 현재 활성 사용자 수 계산
  - [ ] 진행 중인 테스트 통계
  
**커밋 메시지**: `feat: implement real-time statistics API endpoints`

### 3.5 결과 분포 통계 API (1.5시간)
- [ ] **결과 통계 엔드포인트**
  - [ ] `/api/stats/results` 구현
  - [ ] 결과 유형별 분포 계산
  - [ ] 시간대별 통계 집계
  
**커밋 메시지**: `feat: add quiz results distribution statistics API`

### 3.6 관리자 대시보드 - 기본 페이지 (1시간)
- [ ] **대시보드 HTML 템플릿**
  - [ ] `templates/admin/dashboard.html` 생성
  - [ ] 기본 레이아웃 및 네비게이션
  - [ ] Chart.js 라이브러리 추가
  
**커밋 메시지**: `feat: create admin dashboard basic HTML template`

### 3.7 관리자 대시보드 - 실시간 차트 (2시간)
- [ ] **실시간 차트 구현**
  - [ ] JavaScript 차트 렌더링
  - [ ] API 데이터 연동
  - [ ] 자동 새로고침 기능
  
**커밋 메시지**: `feat: implement real-time charts in admin dashboard`

---

## 🛠️ 4. 기술 인프라 개선

### 4.1 E2E 테스트 - 환경 설정 (1시간)
- [ ] **Playwright 의존성 추가**
  - [ ] pyproject.toml에 playwright 추가
  - [ ] 테스트 설정 파일 생성
  - [ ] 별도 프로세스 실행 스크립트
  
**커밋 메시지**: `feat: setup Playwright E2E testing environment`

### 4.2 E2E 테스트 - 기본 시나리오 (2시간)
- [ ] **핵심 사용자 플로우 테스트**
  - [ ] 퀴즈 시작 → 완료 → 결과 시나리오
  - [ ] 공유 버튼 존재 여부 확인
  - [ ] 광고 슬롯 렌더링 검증
  
**커밋 메시지**: `feat: implement basic E2E test scenarios`

### 4.3 성능 최적화 - 이미지 최적화 (1시간)
- [ ] **이미지 최적화 구현**
  - [ ] 이미지 압축 및 WebP 변환
  - [ ] Lazy loading 구현
  - [ ] 적응형 이미지 크기 조정
  
**커밋 메시지**: `feat: optimize images with compression and lazy loading`

### 4.4 보안 강화 - CSP 헤더 (1시간)
- [ ] **보안 헤더 추가**
  - [ ] Content Security Policy 설정
  - [ ] HTTPS 강제 리다이렉트
  - [ ] XSS 방어 헤더 추가
  
**커밋 메시지**: `feat: add security headers and CSP configuration`

### 4.5 Rate Limiting 구현 (1.5시간)
- [ ] **API 요청 제한**
  - [ ] slowapi 라이브러리 추가
  - [ ] 사용자별 요청 제한 설정
  - [ ] Rate limit 초과 시 응답 처리
  
**커밋 메시지**: `feat: implement API rate limiting for security`

---

## 📝 5. 문서화 및 배포

### 5.1 환경변수 문서화 (30분)
- [ ] **환경 설정 가이드**
  - [ ] README.md 환경변수 섹션 업데이트
  - [ ] .env.example 파일 생성
  - [ ] Render.com 설정 가이드 추가
  
**커밋 메시지**: `docs: add environment variables configuration guide`

### 5.2 API 문서 생성 (1시간)
- [ ] **통계 API 문서**
  - [ ] OpenAPI 스키마 추가
  - [ ] API 엔드포인트 문서화
  - [ ] 예제 요청/응답 추가
  
**커밋 메시지**: `docs: create statistics API documentation`

### 5.3 모니터링 헬스체크 강화 (1시간)
- [ ] **헬스체크 개선**
  - [ ] `/health` 엔드포인트 상세화
  - [ ] DB 연결 상태 확인
  - [ ] 외부 API 연결 상태 확인
  
**커밋 메시지**: `feat: enhance health check endpoint with detailed status`

---

## 📅 세분화된 구현 일정 (3주, 총 34개 단계)

### 🗓️ Week 1: 공유 기능 (7개 단계, 8.5시간)
1. 카카오톡 공유 - 기본 구조 설정 (1시간)
2. 카카오톡 공유 - 핵심 JavaScript 구현 (1.5시간)  
3. 카카오톡 공유 - 동적 콘텐츠 생성 (2시간)
4. 카카오톡 공유 - 이벤트 로깅 (1시간)
5. 네이버 밴드 공유 - 기본 모듈 생성 (1시간)
6. 네이버 밴드 공유 - UI 통합 (1.5시간)
7. 공유 기능 - 메타데이터 최적화 (1시간)

### 🗓️ Week 2: 광고 & 통계 기능 (13개 단계, 17시간)
**광고 기능 (6개 단계)**
8. Google AdSense - 환경 설정 (30분)
9. Google AdSense - Stub 제거 및 실제 코드 통합 (1시간)
10. Google AdSense - 광고 슬롯 구현 (1.5시간)
11. Kakao AdFit - 기본 설정 (1시간)
12. A/B 테스트 - 광고 로테이션 구현 (2시간)
13. 광고 성과 측정 - 기본 로깅 (1시간)

**통계 기능 (7개 단계)**
14. Google Analytics 4 - 기본 설정 (1시간)
15. GA4 - 커스텀 이벤트 구현 (1.5시간)
16. 통계 API - 기본 구조 (1시간)
17. 실시간 통계 API - 구현 (2시간)
18. 결과 분포 통계 API (1.5시간)
19. 관리자 대시보드 - 기본 페이지 (1시간)
20. 관리자 대시보드 - 실시간 차트 (2시간)

### 🗓️ Week 3: 인프라 & 문서화 (14개 단계, 14.5시간)
**기술 인프라 (8개 단계)**
21. E2E 테스트 - 환경 설정 (1시간)
22. E2E 테스트 - 기본 시나리오 (2시간)
23. 성능 최적화 - 이미지 최적화 (1시간)
24. 보안 강화 - CSP 헤더 (1시간)
25. Rate Limiting 구현 (1.5시간)

**문서화 & 배포 (3개 단계)**
26. 환경변수 문서화 (30분)
27. API 문서 생성 (1시간)
28. 모니터링 헬스체크 강화 (1시간)

---

## 🏆 Phase 2 성공 지표

### 비즈니스 KPI
- [ ] **사용자 참여**: 공유율 20% 이상 달성
- [ ] **수익화**: 광고 수익 월 $50 이상 달성
- [ ] **성장**: MAU(월 활성 사용자) 1,000명 달성
- [ ] **품질**: 사용자 만족도 4.5/5.0 이상

### 기술 KPI
- [ ] **성능**: 페이지 로딩 시간 2초 이하 유지
- [ ] **안정성**: 서버 가동률 99.9% 이상
- [ ] **품질**: E2E 테스트 커버리지 80% 이상
- [ ] **보안**: 보안 취약점 0개 유지

---

**✨ 세분화 완료!**
- 📊 **총 28개 구현 단계** (각 1-2시간 분량)
- ⏱️ **예상 총 개발시간**: 약 40시간 (3주)
- 💬 **각 단계별 커밋 메시지** 제공
- 🎯 **커서로 한 번에 구현 가능한 크기**로 최적화 