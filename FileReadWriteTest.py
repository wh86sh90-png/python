# FileReadWriteTest.py

# demo.txt 파일에 쓰기: Write text
f = open("demo.txt", "wt", encoding="utf-8")
f.write("Hello, File!\n")
f.write("This is a test file.\n")
f.write("Goodbye, File!\n")
f.close()

# demo.txt 파일에서 읽기: Read text
f = open("demo.txt", "rt", encoding="utf-8")
# read() 파일의 끝까지 읽기를 해서 문자열 변수로 리턴
content = f.read()
print(content)
f.close()
