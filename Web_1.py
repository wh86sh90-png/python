# Web_1.py

from bs4 import BeautifulSoup

# 파일 로딩
page = open("Chap09_test.html", "rt", encoding="utf-8").read()

# 검색이 용이한 객체 생성
soup = BeautifulSoup(page, "html.parser")

# 전체를 출력
# print(soup.prettify())
# <p> 태그를 모두 검색
# plist = soup.find_all("p")
# for p in plist:
#     print(p)
# p = soup.find("p")
# print(p)
# p = soup.find_all("p", class_="outer-text")
# for item in p:
#     print(item)

p = soup.find_all("p", attrs={'class' : "outer-text"})
for item in p:
    print(item)

for item in p:
    title = item.text.strip()
    title = title.replace("\n", " ")
    print(title)
    
