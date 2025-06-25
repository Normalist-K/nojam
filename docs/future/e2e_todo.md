# E2E 테스트 TODO

## 현재 상태
- 단위 테스트 7개 모두 통과
- E2E 테스트는 v0.1.0에서 제외하고 TODO로 남김

## 해결해야 할 문제들

### 1. Playwright 비동기 루프 충돌
- FastAPI TestClient와 Playwright의 async 이벤트 루프가 충돌하는 문제
- 현재 테스트 실행 시 hang 현상 발생

### 2. 해결 전략 (v0.2.0에서 구현 예정)

#### 옵션 A: 별도 프로세스 전략
```python
# 서버를 별도 프로세스로 실행하고 Playwright로 접근
import subprocess
import time

def test_e2e_flow():
    # 1. 서버 프로세스 시작
    server = subprocess.Popen(['uv', 'run', 'uvicorn', 'nojam.main:app', '--port', '8001'])
    time.sleep(2)  # 서버 시작 대기
    
    # 2. Playwright로 실제 브라우저 테스트
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:8001/quiz')
        # ... 테스트 로직
        browser.close()
    
    # 3. 서버 프로세스 종료
    server.terminate()
```

#### 옵션 B: httpx + 기본 HTML 파싱
```python
# Playwright 대신 httpx로 HTTP 테스트, BeautifulSoup으로 HTML 검증
import httpx
from bs4 import BeautifulSoup

async def test_quiz_flow():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        # 퀴즈 페이지 접근
        response = await client.get("/quiz")
        soup = BeautifulSoup(response.text, 'html.parser')
        assert soup.find('form', {'action': '/submit'})
        
        # 폼 제출
        form_data = {f"q{i}": "A" for i in range(1, 11)}
        response = await client.post("/submit", data=form_data, follow_redirects=False)
        assert response.status_code == 302
```

## 구현 계획

### v0.2.0 목표
- [ ] Playwright 환경 분리 (별도 프로세스)
- [ ] 전체 사용자 플로우 E2E 테스트
- [ ] 카카오 공유 Stub 호출 테스트
- [ ] AdSense div 렌더링 검증
- [ ] CI/CD에서 E2E 테스트 자동 실행

### 테스트 시나리오
1. 퀴즈 페이지 접근 → 10문항 모두 표시
2. 모든 문항 선택 후 제출 → 결과 페이지 리다이렉트
3. 결과 페이지에서 카드 이미지, 광고 슬롯, 공유 버튼 확인
4. 카카오 공유 버튼 클릭 → Stub API 호출 성공

## 참고 자료
- [Playwright Python 공식 문서](https://playwright.dev/python/)
- [FastAPI 테스팅 가이드](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest-playwright 플러그인](https://pytest-playwright.readthedocs.io/) 