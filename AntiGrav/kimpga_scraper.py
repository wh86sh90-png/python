"""
김프가(kimpga.com) 상위 코인 20개 크롤링 스크립트
Selenium을 사용하여 동적 콘텐츠를 로드하고 데이터를 추출합니다.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
from datetime import datetime


class KimpgaScraper:
    """김프가 웹사이트에서 암호화폐 데이터를 크롤링하는 클래스"""
    
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
        """Chrome WebDriver 설정"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
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
            print(f"🌐 {self.url} 접속 중...")
            
            # 페이지 로드
            self.driver.get(self.url)
            
            # 페이지가 완전히 로드될 때까지 대기
            print("⏳ 페이지 로딩 대기 중...")
            time.sleep(5)  # 동적 콘텐츠 로드를 위한 대기
            
            # 코인 데이터 추출
            coins_data = []
            
            # 여러 가능한 선택자를 시도
            selectors = [
                "div[role='row']",  # Material-UI 테이블 행
                "tr",  # 일반 테이블 행
                "div.MuiTableRow-root",  # Material-UI 특정 클래스
            ]
            
            rows = []
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 1:  # 헤더 제외하고 데이터가 있는지 확인
                        rows = elements
                        print(f"✅ '{selector}' 선택자로 {len(rows)}개 요소 발견")
                        break
                except Exception as e:
                    continue
            
            if not rows:
                print("⚠️ 테이블 행을 찾을 수 없습니다. 페이지 구조를 분석합니다...")
                # 페이지 소스 일부 출력 (디버깅용)
                page_source = self.driver.page_source[:2000]
                print(f"페이지 소스 샘플:\n{page_source}")
                return []
            
            print(f"📊 상위 {num_coins}개 코인 데이터 추출 중...")
            
            # 각 행에서 데이터 추출
            count = 0
            for idx, row in enumerate(rows):
                if count >= num_coins:
                    break
                
                try:
                    # 행의 텍스트 내용 가져오기
                    row_text = row.text.strip()
                    
                    # 빈 행이나 헤더 행 건너뛰기
                    if not row_text or '순위' in row_text or '코인명' in row_text:
                        continue
                    
                    # 행 내의 모든 셀 찾기
                    cells = row.find_elements(By.CSS_SELECTOR, "div, td, span")
                    
                    # 코인 이름과 심볼 찾기
                    coin_name = ""
                    coin_symbol = ""
                    
                    # 이미지 태그로 코인 식별
                    try:
                        img = row.find_element(By.TAG_NAME, "img")
                        # 이미지가 있으면 코인 행으로 간주
                        
                        # 텍스트에서 코인 정보 추출
                        text_parts = row_text.split('\n')
                        
                        if len(text_parts) >= 2:
                            # 일반적으로 첫 번째는 한글명, 두 번째는 심볼
                            for part in text_parts:
                                if part and not any(char.isdigit() for char in part[:3]):
                                    if not coin_name:
                                        coin_name = part
                                    elif not coin_symbol and part != coin_name:
                                        coin_symbol = part
                                        break
                        
                        coin_data = {
                            '순위': count + 1,
                            '코인명': coin_name,
                            '심볼': coin_symbol,
                            '원문 데이터': row_text,
                            '수집 시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        # 가격 정보 추출 시도 (숫자가 포함된 부분)
                        prices = []
                        for part in text_parts:
                            if any(char.isdigit() for char in part):
                                prices.append(part)
                        
                        if prices:
                            coin_data['가격 정보'] = ' | '.join(prices[:3])  # 처음 3개 가격 정보
                        
                        coins_data.append(coin_data)
                        count += 1
                        
                        print(f"  {count}. {coin_name} ({coin_symbol})")
                        
                    except:
                        # 이미지가 없으면 코인 행이 아님
                        continue
                        
                except Exception as e:
                    print(f"⚠️ 행 {idx} 처리 중 오류: {str(e)}")
                    continue
            
            print(f"\n✅ 총 {len(coins_data)}개 코인 데이터 수집 완료!")
            return coins_data
            
        except Exception as e:
            print(f"❌ 크롤링 중 오류 발생: {str(e)}")
            return []
            
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 브라우저 종료")
    
    def save_to_csv(self, data, filename='kimpga_top20_coins.csv'):
        """
        데이터를 CSV 파일로 저장
        
        Args:
            data (list): 코인 데이터 리스트
            filename (str): 저장할 파일명
        """
        if not data:
            print("⚠️ 저장할 데이터가 없습니다.")
            return
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"💾 데이터가 '{filename}' 파일로 저장되었습니다.")
        
    def save_to_excel(self, data, filename='kimpga_top20_coins.xlsx'):
        """
        데이터를 Excel 파일로 저장
        
        Args:
            data (list): 코인 데이터 리스트
            filename (str): 저장할 파일명
        """
        if not data:
            print("⚠️ 저장할 데이터가 없습니다.")
            return
        
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"💾 데이터가 '{filename}' 파일로 저장되었습니다.")


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🪙  김프가(kimpga.com) 상위 코인 크롤러")
    print("=" * 60)
    print()
    
    # 스크래퍼 인스턴스 생성 (headless=False로 설정하면 브라우저가 보임)
    scraper = KimpgaScraper(headless=False)
    
    # 상위 20개 코인 크롤링
    coins = scraper.scrape_top_coins(num_coins=20)
    
    # 결과 출력
    if coins:
        print("\n" + "=" * 60)
        print("📋 수집된 데이터:")
        print("=" * 60)
        for coin in coins:
            print(f"\n{coin['순위']}. {coin['코인명']} ({coin['심볼']})")
            if '가격 정보' in coin:
                print(f"   가격: {coin['가격 정보']}")
            print(f"   원문: {coin['원문 데이터'][:100]}...")
        
        # CSV 파일로 저장
        scraper.save_to_csv(coins)
        
        # Excel 파일로 저장 (openpyxl 설치 필요)
        try:
            scraper.save_to_excel(coins)
        except ImportError:
            print("ℹ️  Excel 저장을 위해서는 'openpyxl' 패키지가 필요합니다.")
            print("   설치: pip install openpyxl")
    else:
        print("\n⚠️ 데이터를 수집하지 못했습니다.")
    
    print("\n" + "=" * 60)
    print("✨ 프로그램 종료")
    print("=" * 60)


if __name__ == "__main__":
    main()
