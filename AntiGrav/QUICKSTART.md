# 🚀 김프가 크롤러 - 빠른 시작 가이드

## GUI 버전 (추천)

### 실행
```bash
python kimpga_scraper_gui.py
```

### 사용법
1. 프로그램 실행
2. 코인 개수 설정 (기본: 20개)
3. "🚀 크롤링 시작" 버튼 클릭
4. 완료 후 "📄 CSV로 저장" 또는 "📊 Excel로 저장" 클릭

### 특징
- ✅ 사용하기 쉬운 GUI
- ✅ 실시간 진행 상황 표시
- ✅ 언제든지 중지 가능
- ✅ 데이터 테이블로 확인
- ✅ CSV/Excel 저장

---

## 명령줄 버전

### 실행
```bash
python kimpga_scraper_v2.py
```

### 특징
- ✅ 자동화에 적합
- ✅ 스크립트로 실행 가능
- ✅ 서버 환경에서 사용 가능

---

## 설치

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. Chrome 설치
- Chrome 브라우저 필요
- ChromeDriver는 자동 설치됨

---

## 파일 구조

```
📁 AntiGrav/
├── 📄 kimpga_scraper_gui.py      # GUI 버전 (추천)
├── 📄 kimpga_scraper_v2.py       # 명령줄 버전
├── 📄 requirements.txt           # 필요한 패키지
├── 📄 README_GUI.md              # GUI 상세 가이드
└── 📄 QUICKSTART.md              # 이 파일
```

---

## 문제 해결

### PyQt5가 없다는 오류
```bash
pip install PyQt5
```

### Chrome 드라이버 오류
- Chrome 브라우저 최신 버전 설치
- 인터넷 연결 확인

### 데이터가 안 나올 때
- 백그라운드 모드 해제
- 웹사이트 접속 확인
- 잠시 후 다시 시도

---

## 💡 팁

1. **처음 사용**: 5~10개 코인으로 테스트
2. **빠른 실행**: 백그라운드 모드 사용
3. **디버깅**: 백그라운드 모드 해제하고 브라우저 확인
4. **정기 수집**: 명령줄 버전 + 스케줄러 사용

---

**즐거운 크롤링 되세요! 🎉**
