# 김프가(kimpga.com) 코인 크롤러

김프가 웹사이트에서 상위 20개 암호화폐의 김치프리미엄 정보를 크롤링하는 Python 스크립트입니다.

## 📋 기능

- 상위 20개 코인의 실시간 데이터 수집
- 코인명, 심볼, 가격, 김치프리미엄 정보 추출
- CSV 및 Excel 파일로 데이터 저장
- 자동 ChromeDriver 관리

## 🔧 설치 방법

### 1. 필수 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. Chrome 브라우저 설치
- Google Chrome 브라우저가 설치되어 있어야 합니다
- ChromeDriver는 자동으로 다운로드됩니다 (webdriver-manager 사용)

## 🚀 사용 방법

### 기본 실행 (v2 권장)

```bash
python kimpga_scraper_v2.py
```

### 버전 1 실행

```bash
python kimpga_scraper.py
```

## 📊 출력 파일

실행 후 다음 파일들이 생성됩니다:

- `kimpga_top20_coins.csv` - CSV 형식의 데이터
- `kimpga_top20_coins.xlsx` - Excel 형식의 데이터

## 📁 파일 설명

### kimpga_scraper.py
- 기본 버전 스크래퍼
- Selenium을 사용한 동적 콘텐츠 크롤링

### kimpga_scraper_v2.py (권장)
- 개선된 버전
- BeautifulSoup과 Selenium 결합
- 더 안정적인 데이터 추출
- 자동 ChromeDriver 관리
- 상세한 에러 처리

## ⚙️ 설정 옵션

코드 내에서 다음 옵션을 변경할 수 있습니다:

```python
# 브라우저 표시 여부
scraper = KimpgaScraperV2(headless=False)  # 브라우저 표시
scraper = KimpgaScraperV2(headless=True)   # 백그라운드 실행

# 크롤링할 코인 개수
coins = scraper.scrape_top_coins(num_coins=20)  # 20개
coins = scraper.scrape_top_coins(num_coins=50)  # 50개
```

## 🔍 수집 데이터 항목

- **순위**: 코인 순위
- **코인명**: 코인의 한글 이름
- **심볼**: 코인 심볼 (예: BTC, ETH)
- **국내가격**: 국내 거래소 가격
- **해외가격**: 해외 거래소 가격
- **김프율**: 김치프리미엄 비율
- **김프액**: 김치프리미엄 금액
- **수집시간**: 데이터 수집 시간

## 🐛 문제 해결

### ChromeDriver 오류
```bash
# webdriver-manager 재설치
pip install --upgrade webdriver-manager
```

### 데이터를 찾을 수 없는 경우
- `headless=False`로 설정하여 브라우저 동작 확인
- 인터넷 연결 확인
- 웹사이트 접근 가능 여부 확인

### Excel 저장 오류
```bash
# openpyxl 설치 확인
pip install openpyxl
```

## 📝 주의사항

- 웹 크롤링은 해당 웹사이트의 이용약관을 준수해야 합니다
- 과도한 요청은 서버에 부담을 줄 수 있으므로 적절한 간격을 두고 실행하세요
- 웹사이트 구조 변경 시 스크립트 수정이 필요할 수 있습니다

## 📄 라이선스

개인 및 교육 목적으로 자유롭게 사용 가능합니다.

## 🤝 기여

버그 리포트나 개선 제안은 언제든 환영합니다!
