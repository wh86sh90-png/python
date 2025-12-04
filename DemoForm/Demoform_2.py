# Demoform.py

# Demoform.ui(화면단), Demoform.py(로직단) = Demoform 완성

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *

from bs4 import BeautifulSoup

import urllib.request

# 디자인 문서를 로딩
form_class = uic.loadUiType("DemoForm/Demoform_2.ui")[0]

# Demoform 클래스 정의
class Demoform(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.label.setText("안녕하세요 PyQt5")

        # 버튼 클릭 시 동작할 함수 연결
        #self.pushButton.clicked.connect(self.btnClicked)

    # def btnClicked(self):
    #     # 라벨의 텍스트를 변경
    #     self.label.setText("버튼이 클릭되었습니다.")
    def firstClick(self):
        f = open("clien.txt", "wt", encoding="utf-8")

        for page_num in range(0, 10):
    # url = "https://www.clien.net/service/board/sold"
            url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(page_num)
            print(url)

    # 페이지 실행 결과를 문자열로 받기
            page = urllib.request.urlopen(url).read().decode("utf-8")
    # 검색이 용이한 객체 생성
            soup = BeautifulSoup(page, "html.parser")

    # date-role 속성이 list-title-text 인  span 태그를 모두 검색
            lst = soup.find_all("span", attrs={"data-role":"list-title-text"})
            for tag in lst:
                title = tag.text.strip()
                f.write(title + "\n")
                print(title)


# 파일 닫기
        f.close()
        self.label.setText("첫 번째 버튼이 클릭되었습니다.")

    def secondClick(self):
        self.label.setText("두 번째 버튼이 클릭되었습니다.")
    
    def thirdClick(self):
        self.label.setText("세 번째 버튼이 클릭되었습니다.")


# 진입점
if __name__ == "__main__":
    # 실행 프로세스를 생성
    app = QApplication(sys.argv)
    # 폼을 생성
    demoform = Demoform()
    # 화면 출력
    demoform.show()
    # 계속 대기(이벤트 루프)
    sys.exit(app.exec_())
