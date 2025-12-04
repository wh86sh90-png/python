from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def crawl_naver_news_selenium(url):
    """
    Selenium을 사용하여 네이버 검색 결과에서 뉴스 기사 제목을 크롤링하는 함수
    
    Args:
        url (str): 네이버 검색 결과 URL
    
    Returns:
        list: 뉴스 기사 제목 리스트
    """
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저 창 숨김
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    driver = None
    news_titles = []
    
    try:
        # WebDriver 초기화 (자동으로 ChromeDriver 다운로드)
        print("ChromeDriver 초기화 중...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 페이지 로드
        print("페이지 로딩 중...")
        driver.get(url)
        
        # 페이지 로드 대기
        time.sleep(3)
        
        # 뉴스 영역이 로드될 때까지 대기
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.news_tit, .news_area"))
            )
        except:
            print("뉴스 영역을 찾을 수 없습니다.")
        
        # 여러 선택자 시도
        selectors = [
            "a.news_tit",  # 가장 일반적인 뉴스 제목 링크
            ".news_area .news_tit",
            ".api_subject_bx a.news_tit",
            ".total_wrap .news_area a",
            ".news_wrap .news_area a.news_tit"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"선택자 '{selector}'로 {len(elements)}개의 요소를 찾았습니다.")
                    for element in elements:
                        try:
                            # title 속성 또는 텍스트 가져오기
                            title = element.get_attribute('title') or element.text.strip()
                            if title and title not in news_titles:
                                news_titles.append(title)
                        except:
                            continue
                    
                    if news_titles:
                        break  # 제목을 찾았으면 중단
            except Exception as e:
                continue
        
        return news_titles
    
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return []
    
    finally:
        if driver:
            driver.quit()


def main():
    # 크롤링할 URL
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%95%84%EC%9D%B4%ED%8F%B017&ackey=r45v88ak"
    
    print("=" * 80)
    print("네이버 뉴스 크롤링 시작 (Selenium 사용)")
    print("=" * 80)
    print(f"URL: {url}\n")
    
    # 뉴스 제목 크롤링
    titles = crawl_naver_news_selenium(url)
    
    # 결과 출력
    if titles:
        print(f"\n총 {len(titles)}개의 뉴스 기사를 찾았습니다.\n")
        print("=" * 80)
        for idx, title in enumerate(titles, 1):
            print(f"{idx}. {title}")
            print("-" * 80)
    else:
        print("\n뉴스 기사를 찾지 못했습니다.")


if __name__ == "__main__":
    main()
