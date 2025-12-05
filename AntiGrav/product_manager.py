import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt


class ProductManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_db()
        self.init_ui()
        self.load_data()
        
    def init_db(self):
        """데이터베이스 및 테이블 초기화"""
        self.conn = sqlite3.connect('MyProducts.db')
        self.cursor = self.conn.cursor()
        
        # Products 테이블 생성 (존재하지 않을 경우)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                prodID INTEGER PRIMARY KEY AUTOINCREMENT,
                prodName TEXT NOT NULL,
                prodPrice INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('전자제품 관리 프로그램')
        self.setGeometry(100, 100, 800, 600)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 입력 폼 영역
        form_layout = QVBoxLayout()
        
        # ID 입력 (수정/삭제 시 사용)
        id_layout = QHBoxLayout()
        id_label = QLabel('제품 ID:')
        id_label.setFixedWidth(80)
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setPlaceholderText('자동 생성')
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.id_input)
        form_layout.addLayout(id_layout)
        
        # 제품명 입력
        name_layout = QHBoxLayout()
        name_label = QLabel('제품명:')
        name_label.setFixedWidth(80)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('제품명을 입력하세요')
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)
        
        # 가격 입력
        price_layout = QHBoxLayout()
        price_label = QLabel('가격:')
        price_label.setFixedWidth(80)
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText('가격을 입력하세요')
        price_layout.addWidget(price_label)
        price_layout.addWidget(self.price_input)
        form_layout.addLayout(price_layout)
        
        main_layout.addLayout(form_layout)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        self.insert_btn = QPushButton('입력')
        self.insert_btn.clicked.connect(self.insert_product)
        
        self.update_btn = QPushButton('수정')
        self.update_btn.clicked.connect(self.update_product)
        
        self.delete_btn = QPushButton('삭제')
        self.delete_btn.clicked.connect(self.delete_product)
        
        self.search_btn = QPushButton('검색')
        self.search_btn.clicked.connect(self.search_product)
        
        self.clear_btn = QPushButton('초기화')
        self.clear_btn.clicked.connect(self.clear_inputs)
        
        button_layout.addWidget(self.insert_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.search_btn)
        button_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(button_layout)
        
        # 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['제품 ID', '제품명', '가격'])
        
        # 테이블 헤더 설정
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # 더블클릭 이벤트 연결
        self.table.cellDoubleClicked.connect(self.on_row_double_clicked)
        
        main_layout.addWidget(self.table)
        
    def load_data(self, search_name=None):
        """데이터베이스에서 데이터 로드"""
        if search_name:
            self.cursor.execute('SELECT * FROM Products WHERE prodName LIKE ?', 
                              (f'%{search_name}%',))
        else:
            self.cursor.execute('SELECT * FROM Products ORDER BY prodID')
        
        rows = self.cursor.fetchall()
        
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)
    
    def insert_product(self):
        """제품 추가"""
        name = self.name_input.text().strip()
        price = self.price_input.text().strip()
        
        if not name or not price:
            QMessageBox.warning(self, '입력 오류', '제품명과 가격을 모두 입력해주세요.')
            return
        
        try:
            price = int(price)
        except ValueError:
            QMessageBox.warning(self, '입력 오류', '가격은 숫자로 입력해주세요.')
            return
        
        try:
            self.cursor.execute('INSERT INTO Products (prodName, prodPrice) VALUES (?, ?)',
                              (name, price))
            self.conn.commit()
            QMessageBox.information(self, '성공', '제품이 추가되었습니다.')
            self.clear_inputs()
            self.load_data()
        except sqlite3.Error as e:
            QMessageBox.critical(self, '오류', f'데이터베이스 오류: {str(e)}')
    
    def update_product(self):
        """제품 수정"""
        prod_id = self.id_input.text().strip()
        name = self.name_input.text().strip()
        price = self.price_input.text().strip()
        
        if not prod_id:
            QMessageBox.warning(self, '입력 오류', '수정할 제품을 선택해주세요.')
            return
        
        if not name or not price:
            QMessageBox.warning(self, '입력 오류', '제품명과 가격을 모두 입력해주세요.')
            return
        
        try:
            price = int(price)
            prod_id = int(prod_id)
        except ValueError:
            QMessageBox.warning(self, '입력 오류', '가격과 ID는 숫자로 입력해주세요.')
            return
        
        try:
            self.cursor.execute('UPDATE Products SET prodName=?, prodPrice=? WHERE prodID=?',
                              (name, price, prod_id))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                QMessageBox.information(self, '성공', '제품이 수정되었습니다.')
                self.clear_inputs()
                self.load_data()
            else:
                QMessageBox.warning(self, '오류', '해당 ID의 제품을 찾을 수 없습니다.')
        except sqlite3.Error as e:
            QMessageBox.critical(self, '오류', f'데이터베이스 오류: {str(e)}')
    
    def delete_product(self):
        """제품 삭제"""
        prod_id = self.id_input.text().strip()
        
        if not prod_id:
            QMessageBox.warning(self, '입력 오류', '삭제할 제품을 선택해주세요.')
            return
        
        try:
            prod_id = int(prod_id)
        except ValueError:
            QMessageBox.warning(self, '입력 오류', 'ID는 숫자여야 합니다.')
            return
        
        reply = QMessageBox.question(self, '삭제 확인', 
                                     f'제품 ID {prod_id}를 삭제하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute('DELETE FROM Products WHERE prodID=?', (prod_id,))
                self.conn.commit()
                
                if self.cursor.rowcount > 0:
                    QMessageBox.information(self, '성공', '제품이 삭제되었습니다.')
                    self.clear_inputs()
                    self.load_data()
                else:
                    QMessageBox.warning(self, '오류', '해당 ID의 제품을 찾을 수 없습니다.')
            except sqlite3.Error as e:
                QMessageBox.critical(self, '오류', f'데이터베이스 오류: {str(e)}')
    
    def search_product(self):
        """제품 검색"""
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, '입력 오류', '검색할 제품명을 입력해주세요.')
            return
        
        self.load_data(search_name=name)
        
        if self.table.rowCount() == 0:
            QMessageBox.information(self, '검색 결과', '검색 결과가 없습니다.')
    
    def clear_inputs(self):
        """입력 필드 초기화"""
        self.id_input.clear()
        self.name_input.clear()
        self.price_input.clear()
        self.load_data()  # 전체 데이터 다시 로드
    
    def on_row_double_clicked(self, row, column):
        """테이블 행 더블클릭 시 입력창에 데이터 복사"""
        prod_id = self.table.item(row, 0).text()
        prod_name = self.table.item(row, 1).text()
        prod_price = self.table.item(row, 2).text()
        
        self.id_input.setText(prod_id)
        self.name_input.setText(prod_name)
        self.price_input.setText(prod_price)
    
    def closeEvent(self, event):
        """프로그램 종료 시 데이터베이스 연결 종료"""
        self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProductManager()
    window.show()
    sys.exit(app.exec_())
