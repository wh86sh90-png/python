# WebEditCroniong.py

# coding:utf-8
from bs4 import BeautifulSoup
import urllib.request

# 정규표현식 사용
import re 

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

f = open("todayhumor.txt", "wt", encoding="utf-8")
# <td class="subject">
# <a href="/board/view.php?table=bestofbest&amp;no=481397&amp;s_no=481397&amp;page=1" target="_top">아이유 삼행시 대참사</a>
# <span class="list_memo_count_span"> [8]</span>]
# <span style="margin-left:4px;">
# <img src="//www.todayhumor.co.kr/board/images/list_icon_photo.gif" style="vertical-align:middle; margin-bottom:1px;">
# </span>
# <img src="//www.todayhumor.co.kr/board/images/list_icon_shovel.gif?2" alt="펌글" style="margin-right:3px;top:2px;position:relative"> 
# </td>

for n in range(0,10):
    #오늘의 유머 베스트 주소 
    data ='https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=' + str(n)
    print(data)
    #웹브라우져 헤더 추가 
    req = urllib.request.Request(data, headers = hdr)
    data = urllib.request.urlopen(req).read()
    #한글이 깨지는 경우
    page = data.decode('utf-8', 'ignore')
    soup = BeautifulSoup(page, 'html.parser')
    list = soup.find_all('td', attrs={'class':'subject'})

    for item in list:
        try:
                title = item.find('a').text.strip()
                if re.search('아이유', title):
                        print(title)
                        f.write(title + "\n")
                #<a class='list_subject'><span>text</span><span>text</span>
                # span = item.contents[1]
                # span2 = span.nextSibling.nextSibling
                # title = span2.text 
                # if (re.search('아이폰', title)):
                #         print(title.strip())
                #         print('https://www.clien.net'  + item['href'])
        except:
                pass
    
f.close()
