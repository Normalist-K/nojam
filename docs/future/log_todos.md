# Logging TODOs

이 문서는 향후 로그 시스템을 더 깊이 구현하기 위해 남겨두는 작업 목록입니다.

## TODO 리스트
- [ ] structlog 레벨별 필터 설정 (`info`, `error`, `critical`)
- [ ] GA4 이벤트 로깅 최적화 (batch 처리, 오류 핸들링)
- [ ] 광고 지표 로그 (AdSense, AdFit) 전송 파이프라인 구축
- [ ] 샘플링 비율 조정(100% → 10%) 및 설정값 환경변수화
- [ ] Render Log Streams → 외부 모니터링(예: Datadog, Loki) 연동
- [ ] 스택 트레이스 구조화 및 Trace ID 추가
- [ ] 사용자 에이전트·IP 해시 기반 요청별 로그 메타데이터 강화
- [ ] `/health` 체크 로깅 빈도 감소 또는 필터링 