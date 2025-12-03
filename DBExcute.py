# DBExcute.py

import sqlite3

# 연결 객체 생성
conn = sqlite3.connect(':memory:')  # 메모리 내 임시 데이터베이스 사용

# 커서 객체 생성
cursor = conn.cursor()

# 테이블 생성
cursor.execute("CREATE TABLE PhoneBook (name TEXT, phone TEXT);")

# 데이터 삽입
cursor.execute("INSERT INTO PhoneBook (name, phone) VALUES ('Alice', '123-4567');")
cursor.execute("INSERT INTO PhoneBook (name, phone) VALUES ('Bob', '987-6543');")

# 입력파라메터처리
name = 'Charlie'
phone = '555-0000'
cursor.execute("INSERT INTO PhoneBook (name, phone) VALUES (?, ?);", (name, phone))

# 다중 리스트 입력
datalist = (('Dave', '111-2222'), ('Eve', '333-4444'))
cursor.executemany("INSERT INTO PhoneBook (name, phone) VALUES (?, ?);", datalist)

# 데이터 조회
cursor.execute("SELECT * FROM PhoneBook;")
for row in cursor:
    print(row)

