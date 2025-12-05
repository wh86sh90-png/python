"""
김프가(kimpga.com) 상위 코인 20개 크롤링 스크립트 (개선 버전)
BeautifulSoup과 Selenium을 함께 사용하여 더 안정적으로 데이터를 추출합니다.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import re


class KimpgaScraperV2:
    """김프가 웹사이트에서 암호화폐 데이터를 크롤링하는 클래스 (개선 버전)"""
    
    def __init__(self, headless=True):
        """
        스크래퍼 초기화
        
        Args:
            headless (bool): 브라우저를 백그라운드에서 실행할지 여부
        """
        self.url = "https://kimpga.com/"
        self.driver = None
        self.headless = headless
        
    def setup_driver(self):
        """Chrome WebDriver 설정 (자동 드라이버 관리)"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # webdriver-manager를 사용하여 자동으로 ChromeDriver 설치 및 관리
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def extract_number(self, text):
        """텍스트에서 숫자 추출"""
        if not text:
            return None
        # 숫자, 콤마, 점, 퍼센트, 마이너스 기호만 추출
        numbers = re.findall(r'[-]?[\d,]+\.?\d*%?', text)
        return numbers[0] if numbers else None
    
    def scrape_top_coins(self, num_coins=20):
        """
        상위 N개의 코인 데이터를 크롤링
        
        Args:
            num_coins (int): 크롤링할 코인 개수 (기본값: 20)
            
        Returns:
            list: 코인 데이터 딕셔너리 리스트
        """
        try:
            self.setup_driver()
            print(f"[WEB] {self.url} 접속 중...")
            
            # 페이지 로드
            self.driver.get(self.url)
            
            # 페이지가 완전히 로드될 때까지 대기
            print("[WAIT] 페이지 로딩 대기 중...")
            time.sleep(5)  # 동적 콘텐츠 로드를 위한 대기
            
            # 스크롤하여 모든 데이터 로드
            print("[SCROLL] 페이지 스크롤 중...")
            for _ in range(3):
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(0.5)
            
            # 페이지 소스 가져오기
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 코인 데이터 추출
            coins_data = []
            
            print(f"[DATA] 상위 {num_coins}개 코인 데이터 추출 중...")
            
            # 다양한 방법으로 코인 행 찾기
            # 방법 1: role="row" 속성을 가진 div 찾기
            rows = soup.find_all('div', {'role': 'row'})
            
            if not rows:
                # 방법 2: 테이블 행 찾기
                rows = soup.find_all('tr')
            
            if not rows:
                print("[WARNING] 코인 데이터를 찾을 수 없습니다.")
                return []
            
            print(f"[OK] {len(rows)}개의 행 발견")
            
            count = 0
            for idx, row in enumerate(rows):
                if count >= num_coins:
                    break
                
                try:
                    # 이미지 태그가 있는지 확인 (코인 아이콘)
                    img = row.find('img')
                    if not img:
                        continue
                    
                    # 모든 텍스트 추출
                    row_text = row.get_text(separator='|', strip=True)
                    text_parts = [part.strip() for part in row_text.split('|') if part.strip()]
                    
                    # 헤더 행 건너뛰기
                    if any(keyword in row_text for keyword in ['순위', '코인명', 'Rank', 'Name']):
                        continue
                    
                    # 코인 정보 추출
                    coin_name = ""
                    coin_symbol = ""
                    
                    # span 태그에서 코인명과 심볼 찾기
                    spans = row.find_all('span')
                    for span in spans:
                        span_text = span.get_text(strip=True)
                        if span_text and len(span_text) > 1:
                            if not coin_name and not any(char.isdigit() for char in span_text[:3]):
                                coin_name = span_text
                            elif not coin_symbol and span_text != coin_name and not any(char.isdigit() for char in span_text):
                                coin_symbol = span_text
                                break
                    
                    # 코인명이 없으면 건너뛰기
                    if not coin_name:
                        continue
                    
                    # 기본 데이터 구조
                    coin_data = {
                        '순위': count + 1,
                        '코인명': coin_name,
                        '심볼': coin_symbol if coin_symbol else coin_name,
                        '수집시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # 가격 및 프리미엄 정보 추출
                    # 숫자가 포함된 텍스트 파트 찾기
                    price_info = []
                    for part in text_parts:
                        if re.search(r'\d', part):
                            price_info.append(part)
                    
                    # 가격 정보 할당 (일반적인 순서: 국내가격, 해외가격, 김프율, 김프액)
                    if len(price_info) >= 1:
                        coin_data['국내가격'] = price_info[0]
                    if len(price_info) >= 2:
                        coin_data['해외가격'] = price_info[1]
                    if len(price_info) >= 3:
                        coin_data['김프율'] = price_info[2]
                    if len(price_info) >= 4:
                        coin_data['김프액'] = price_info[3]
                    
                    coins_data.append(coin_data)
                    count += 1
                    
                    # 진행 상황 출력
                    print(f"  {count}. {coin_name} ({coin_symbol})")
                    if '김프율' in coin_data:
                        print(f"      김프율: {coin_data['김프율']}")
                        
                except Exception as e:
                    print(f"[WARNING] 행 {idx} 처리 중 오류: {str(e)}")
                    continue
            
            print(f"\n[OK] 총 {len(coins_data)}개 코인 데이터 수집 완료!")
            return coins_data
            
        except Exception as e:
            print(f"[ERROR] 크롤링 중 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
            
        finally:
            if self.driver:
                self.driver.quit()
                print("[CLOSE] 브라우저 종료")
    
    def save_to_csv(self, data, filename='kimpga_top20_coins.csv'):
        """데이터를 CSV 파일로 저장"""
        if not data:
            print("[WARNING] 저장할 데이터가 없습니다.")
            return
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"[SAVE] 데이터가 '{filename}' 파일로 저장되었습니다.")
        return filename
        
    def save_to_excel(self, data, filename='kimpga_top20_coins.xlsx'):
        """데이터를 Excel 파일로 저장"""
        if not data:
            print("[WARNING] 저장할 데이터가 없습니다.")
            return
        
        df = pd.DataFrame(data)
        
        # Excel 파일로 저장 (스타일 적용)
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='김프가 Top 20')
            
            # 워크시트 가져오기
            worksheet = writer.sheets['김프가 Top 20']
            
            # 열 너비 자동 조정
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"[SAVE] 데이터가 '{filename}' 파일로 저장되었습니다.")
        return filename
    
    def print_summary(self, data):
        """수집된 데이터 요약 출력"""
        if not data:
            return
        
        print("\n" + "=" * 80)
        print("[SUMMARY] 수집 데이터 요약")
        print("=" * 80)
        
        df = pd.DataFrame(data)
        print(f"\n총 코인 수: {len(df)}")
        print(f"수집 시간: {data[0]['수집시간']}")
        
        print("\n상위 5개 코인:")
        print("-" * 80)
        for i, coin in enumerate(data[:5], 1):
            print(f"{i}. {coin['코인명']} ({coin['심볼']})")
            if '국내가격' in coin:
                print(f"   국내가격: {coin['국내가격']}")
            if '김프율' in coin:
                print(f"   김프율: {coin['김프율']}")
            print()


def main():
    """메인 실행 함수"""
    print("=" * 80)
    print("[KIMPGA] 김프가(kimpga.com) 상위 코인 크롤러 v2.0")
    print("=" * 80)
    print()
    
    # 스크래퍼 인스턴스 생성
    # headless=True: 브라우저 창을 표시하지 않음 (백그라운드 실행)
    # headless=False: 브라우저 창을 표시 (디버깅용)
    scraper = KimpgaScraperV2(headless=False)
    
    # 상위 20개 코인 크롤링
    coins = scraper.scrape_top_coins(num_coins=20)
    
    # 결과 처리
    if coins:
        # 요약 정보 출력
        scraper.print_summary(coins)
        
        # CSV 파일로 저장
        csv_file = scraper.save_to_csv(coins)
        
        # Excel 파일로 저장
        try:
            excel_file = scraper.save_to_excel(coins)
        except Exception as e:
            print(f"[WARNING] Excel 저장 중 오류: {str(e)}")
            print("[INFO] 'openpyxl' 패키지 설치 확인: pip install openpyxl")
    else:
        print("\n[WARNING] 데이터를 수집하지 못했습니다.")
        print("[INFO] 문제 해결 방법:")
        print("   1. 인터넷 연결 확인")
        print("   2. 웹사이트 접근 가능 여부 확인")
        print("   3. headless=False로 설정하여 브라우저 동작 확인")
    
    print("\n" + "=" * 80)
    print("[END] 프로그램 종료")
    print("=" * 80)


if __name__ == "__main__":
    main()
