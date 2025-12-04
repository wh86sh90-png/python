import requests
from bs4 import BeautifulSoup
import time

def crawl_naver_news(url):
    """
    네이버 검색 결과에서 뉴스 기사 제목을 크롤링하는 함수
    
    Args:
        url (str): 네이버 검색 결과 URL
    
    Returns:
        list: 뉴스 기사 제목 리스트
    """
    # User-Agent 헤더 설정 (봇 차단 방지)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 페이지 요청
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 에러 체크
        
        # 인코딩 설정
        response.encoding = 'utf-8'
        
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 뉴스 제목을 저장할 리스트
        news_titles = []
        
        # 네이버 뉴스 섹션의 여러 가능한 선택자를 시도
        # 1. 뉴스 영역의 제목 링크 (일반적인 패턴)
        news_links = soup.select('a.news_tit')
        
        if news_links:
            for link in news_links:
                title = link.get('title') or link.get_text(strip=True)
                if title:
                    news_titles.append(title)
        
        # 2. 다른 가능한 선택자 시도
        if not news_titles:
            # API_SUBJECT_BINDER 클래스를 가진 요소
            news_items = soup.select('.news_area .news_contents .news_tit')
            for item in news_items:
                title = item.get_text(strip=True)
                if title:
                    news_titles.append(title)
        
        # 3. 통합검색 뉴스 영역
        if not news_titles:
            news_items = soup.select('.news_wrap .news_area a.news_tit')
            for item in news_items:
                title = item.get('title') or item.get_text(strip=True)
                if title:
                    news_titles.append(title)
        
        # 4. 일반적인 뉴스 제목 패턴
        if not news_titles:
            news_items = soup.select('.total_wrap .news_area .news_tit')
            for item in news_items:
                title = item.get_text(strip=True)
                if title:
                    news_titles.append(title)
        
        return news_titles
    
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")
        return []
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return []


def main():
    # 크롤링할 URL
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%95%84%EC%9D%B4%ED%8F%B017&ackey=r45v88ak"
    
    print("네이버 뉴스 크롤링 시작...")
    print(f"URL: {url}\n")
    
    # 뉴스 제목 크롤링
    titles = crawl_naver_news(url)
    
    # 결과 출력
    if titles:
        print(f"총 {len(titles)}개의 뉴스 기사를 찾았습니다.\n")
        print("=" * 80)
        for idx, title in enumerate(titles, 1):
            print(f"{idx}. {title}")
            print("-" * 80)
    else:
        print("뉴스 기사를 찾지 못했습니다.")
        print("\n참고: 네이버는 동적으로 콘텐츠를 로드할 수 있습니다.")
        print("Selenium을 사용하면 더 정확한 크롤링이 가능합니다.")


if __name__ == "__main__":
    main()
