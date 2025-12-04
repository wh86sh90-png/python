# Demoform.py

# Demoform.ui(화면단), Demoform.py(로직단) = Demoform 완성

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *

# 디자인 문서를 로딩
form_class = uic.loadUiType("DemoForm/Demoform.ui")[0]

# Demoform 클래스 정의
class Demoform(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setText("안녕하세요 PyQt5")

        # 버튼 클릭 시 동작할 함수 연결
        #self.pushButton.clicked.connect(self.btnClicked)

    # def btnClicked(self):
    #     # 라벨의 텍스트를 변경
    #     self.label.setText("버튼이 클릭되었습니다.")

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
