# OSInfo.py

import os
import os.path
import glob

print("운영체제 이름:", os.name)
print("운영체제 환경:", os.environ)

print("-----파일 정보-----")
# \를 \\두번 사용하지 않고 처리
fileName = r"c:\python310\python.exe"

if os.path.exists(fileName):
    print("파일크기:", os.path.getsize(fileName), "바이트")
else:
    print(f"{fileName} 파일이 존재하지 않습니다.")

print("파일명:", os.path.basename(fileName))
print("전체이름:", os.path.abspath("python.exe"))

print("-----파일목록-----")
print(glob.glob(r"c:\work\*.py")) # c:\work 폴더의 .py 파일 목록
for g in glob.glob(r"c:\work\*.py"): 
    print(g)

