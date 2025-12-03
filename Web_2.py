# Web_2.py

from bs4 import BeautifulSoup

import urllib.request


# <span class="subject_fixed" data-role="list-title-text" title="(끌어올림) 맥북프로 M3pro 14인치">
# 							(끌어올림) 맥북프로 M3pro 14인치
# 						</span>

url = "https://www.clien.net/service/board/sold"

# 페이지 실행 결과를 문자열로 받기
page = urllib.request.urlopen(url).read().decode("utf-8")
# 검색이 용이한 객체 생성
soup = BeautifulSoup(page, "html.parser")

# date-role 속성이 list-title-text 인  span 태그를 모두 검색
lst = soup.find_all("span", attrs={"data-role":"list-title-text"})
for tag in lst:
    title = tag.text.strip()
    print(title)