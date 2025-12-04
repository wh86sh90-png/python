from selenium import webdriver as wb
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd

# Chrome 드라이버 실행
driver = wb.Chrome()
driver.get("https://finance.naver.com/sise/sise_index.naver?code=KPI200")

# 페이지 로딩 완료 대기
time.sleep(5)

data = []

# 모든 iframe 순회
iframes = driver.find_elements(By.TAG_NAME, "iframe")
print(f"iframe 개수: {len(iframes)}")

for i, iframe in enumerate(iframes):
    try:
        # iframe으로 전환
        driver.switch_to.frame(iframe)
        time.sleep(1)
        
        # 현재 iframe의 HTML 파싱
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # type_1 테이블 찾기
        table = soup.find('table', {'class': 'type_1'})
        
        if table:
            print(f"iframe {i}에서 type_1 테이블 찾음!")
            rows = table.find_all('tr')[2:]  # 헤더 제외
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 7:
                    item_name = cols[0].find('a')
                    if item_name:
                        item = {
                            '종목명': item_name.text.strip(),
                            '현재가': cols[1].text.strip(),
                            '전일비': cols[2].text.strip(),
                            '등락률': cols[3].text.strip(),
                            '거래량': cols[4].text.strip(),
                            '거래대금': cols[5].text.strip(),
                            '시가총액': cols[6].text.strip()
                        }
                        data.append(item)
            break
        
        # 메인 프레임으로 복귀
        driver.switch_to.default_content()
        
    except Exception as e:
        print(f"iframe {i} 처리 중 오류: {e}")
        driver.switch_to.default_content()

if data:
    df = pd.DataFrame(data)
    print(df)
    df.to_csv('kospi200_index.csv', index=False, encoding='utf-8-sig')
    print(f"\n데이터 저장 완료: {len(data)}개 종목")
else:
    print("데이터를 찾을 수 없습니다.")

driver.quit()