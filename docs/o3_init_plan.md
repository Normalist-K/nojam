# 베이비붐 세대 대상 심리테스트 웹 서비스 — 기획서 v0.2  
*(“마음나이 테스트” 가칭)*  

---

## 1. 프로젝트 개요
| 항목 | 내용 |
|------|------|
| **목표** | ① 50 – 60대를 위한 ‘쉬운’ 세대별 심리검사 제공<br>② 링크 공유로 자연 바이럴 유도<br>③ 결과 페이지 하단 광고(CPC)로 월 **₩100 만+** 수익 |
| **핵심 지표 (KPI)** | - 4주 차 누적 방문자 ≥ **5 만**<br>- 응답 완료율 ≥ **75 %**<br>- 결과 페이지 평균 CTR ≥ **1 %**<br>- 광고 RPM ≥ **₩2 000** |

---

## 2. Target Persona
| 구분 | 내용 |
|------|------|
| 연령 | 1959 – 1975년생 (50 – 66세) |
| 디바이스 | Android 78 %, iOS 22 % |
| 사용 패턴 | 카카오톡·네이버 밴드 공유 빈도 ↑ |
| Pain Point | 작은 글씨·복잡한 회원가입, 낮은 디지털 신뢰도 |

---

## 3. 핵심 가치 제안
1. **0-Click 가입** : 링크만 누르면 즉시 검사 시작  
2. **한 화면-한 질문** : 인지 부하 ↓, 완주율 ↑  
3. **8가지 결과 카드** : 개인화된 이미지 → 카카오톡 썸네일 고정  
4. **또래 평균 비교 차트** : “공유 동기” 강화  

---

## 4. 결과 유형 (8 종)

| 코드 | 유형 이름 | 대표 키워드 | 대표 대사 |
|------|-----------|-------------|-----------|
| `7080` | 7080 감성형 | 통기타·쎄시봉·낭만 | “그땐 말이야, 통기타였지.” |
| `IMF` | IMF 생존형 | 절약·현실·책임 | “빚지는 게 무서운 거야.” |
| `ACT` | 운동권 열혈형 | 정의·정치의식 | “사회 구조를 몰라서 그래.” |
| `DRM` | MBC드라마형 | 가족애·감성 | “가족이 최고지.” |
| `PHONE` | 폰 적응형 | 유튜브·카톡 | “나도 밴드 알아.” |
| `ANA` | 아날로그 고수형 | 필기·신문·규칙 | “스케줄은 수첩에.” |
| `TREND` | 유행 선도형 | 골프웨어·스타일 | “골프웨어가 힙이야~” |
| `JUNK` | 정크컬쳐 수집형 | 레트로·B-급 | “옛날 CF 기억나?” |

---

## 5. 기능 목록 (MVP)

| 구분 | 기능 | 설명 |
|------|------|------|
| **Quiz** | 10문항 (라디오/리커트) | 진행률 표시, 뒤로가기 제한 |
| **점수 계산** | 선택지→유형 1 점 가산 | 최다 득점 1종 반환 |
| **결과 페이지** | OG 태그 + 카드 이미지 8종 | 하단 AdFit/AdSense 1 slot |
| **공유** | Kakao JS SDK | “공유” 클릭 → 카톡 전송 |
| **데이터 수집** | SQLite→Supabase | `answers_json`, `result_type` |
| **어드민 CSV** | `/export` | 주 1회 Looker Studio 분석 |

---

## 6. 화면 흐름
1. **/quiz** (질문 1/10 … 10/10)  
2. **POST /submit** → 점수 계산 & DB 저장  
3. **302 /result/{rid}** (결과 카드 + 광고 + 공유)  
4. **카톡 공유** → 친구 클릭 시 `/result/{rid}` 렌더

---

## 7. 기술 스택
| 레이어 | 도구 | 비고 |
|--------|------|------|
| Front/Back | **FastAPI + Jinja2 + HTMX** | 파이썬 단일 코드베이스 |
| 스타일 | Tailwind CSS (CDN) | 기본 글씨 18 px |
| DB | SQLite → Supabase (PostgreSQL) | SQLModel ORM |
| 호스팅 | Render | GitHub → Docker 자동 배포 |
| 광고 | Kakao AdFit + Google AdSense | 승인 후 AB 테스트 |
| 이미지 | Cloudflare Images | 결과 카드 8장 |
| 분석 | GA4 (`result_generated`) | Looker Studio 대시보드 |
| 테스트 | pytest, Playwright | 3-step 클릭 검증 |

---

## 8. 데이터 모델

```sql
CREATE TABLE answers (
  id          TEXT PRIMARY KEY,       -- UUID
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  answers_json TEXT,                  -- 원본 응답
  result_type TEXT CHECK(
      result_type IN ('7080','IMF','ACT','DRM','PHONE','ANA','TREND','JUNK')
  ),
  ua_hash     CHAR(64)                -- UA+IP SHA-256
);
```

개인정보 최소수집: IP 원문 미저장, 14 일마다 salt 교체 (PIPA/GDPR 대응)

⸻

9. UI·UX 체크리스트
	•	본문 18 px+, 고대비 (#000/#FFF)
	•	버튼·라디오 영역 ≥ 44 × 44 px
	•	“다음” 버튼 하단 중앙 고정
	•	에러/완료 알림은 컬러 블록 + 간결 문구
	•	다크모드 OFF 기본, 토글 제공
	•	모든 주요 액션 2-step 이내

⸻

10. 일정 & 역할 (T = Kick-off)

주차	개발자 (Python)	일반인 A (콘텐츠)	일반인 B (디자인·마케팅)
T	Repo·DB 스키마	질문 10문항 초안	50대 인터뷰 3명
T + 1	/quiz 폼·점수 로직	결과 문구 8종	카드 배경 8장 시안
T + 2	결과 페이지 & OG	본문 교열	카카오 공유 버튼
T + 3	GA4·AdFit·Render 배포	베타 테스트 & 설문	카톡 채널·블로그 개설
T + 4	버그픽스 & 로그	리포트 작성	첫 바이럴 캠페인


⸻

11. 위험요소 & 대응

Risk	영향	대응
광고 승인 지연	수익 지연	초기 AdSense 단독 → AdFit 승인 후 병행
UX 불만 (글씨·버튼)	이탈 ↑	50대 인터뷰 주 3건 → 즉시 수정
트래픽 급증	서버 다운	Supabase + Render autoscaling


⸻

12. 향후 로드맵 (MVP → 3 개월)
	1.	결과 유형 맞춤 뉴스레터 (카톡 비즈메시지)
	2.	친구 매칭 : 같은 결과 유형끼리 연결
	3.	프리미엄 리포트 : LLM 생성 주간 심리 분석 ₩990/월

⸻

이번 주 할 일 (D – D+7)
	•	DB 스키마 & /quiz → /result 플로우 완성
	•	Tailwind Play로 18 px·44 px 가이드 적용
	•	AdFit 매체 등록 신청

⸻

레퍼런스
	•	Kakao AdFit 가이드  https://adfit.kakao.com
	•	Tailwind Play       https://play.tailwindcss.com
	•	Supabase Docs       https://supabase.com/docs

