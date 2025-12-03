# DBExcute.py

import sqlite3

# 연결 객체 생성
conn = sqlite3.connect(r"c:\work\sample.db")

# 커서 객체 생성
cursor = conn.cursor()

# 테이블 생성
# cursor.execute("CREATE TABLE PhoneBook (name TEXT, phone TEXT);")

# 데이터 삽입
# cursor.execute("INSERT INTO PhoneBook (name, phone) VALUES ('Alice', '123-4567');")
# cursor.execute("INSERT INTO PhoneBook (name, phone) VALUES ('Bob', '987-6543');")

# 입력파라메터처리
# name = 'Charlie'
# phone = '555-0000'
# cursor.execute("INSERT INTO PhoneBook (name, phone) VALUES (?, ?);", (name, phone))

# # 다중 리스트 입력
# datalist = (('Dave', '111-2222'), ('Eve', '333-4444'))
# cursor.executemany("INSERT INTO PhoneBook (name, phone) VALUES (?, ?);", datalist)

# 데이터 조회
cursor.execute("SELECT * FROM PhoneBook;")
print("---fetchone()---")
print(cursor.fetchone())  # 한 행만 가져오기
print("---fetchall()---")
print(cursor.fetchall())  # 모든 행 가져오기
print("---fetchmany(2)---")
print(cursor.fetchmany(2))  # 지정한 수만큼 행 가져오기

cursor.execute("SELECT * FROM PhoneBook;")
for row in cursor:
    print(row)

# conn.commit()  # 변경사항 저장
