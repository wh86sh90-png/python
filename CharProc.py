# CharProc.py

strA = "Hello, World!"
strB = "Python Programming"

print(len(strA))
print(len(strB))
print(strA.capitalize())
print(strB.count("P"))

data = "  spam and ham   "
result = data.strip()
print(data)
print(result)

# 치환
result2 = data.replace("spam", "spam egg")
print(result2)

# 리스트로 분할
lst = result2.split()
print(lst)

# 문자열 합치기
joined = ":)".join(lst)
print(joined)   

# 정규표현식: 특정 패턴을 찾아서 바로 작업
import re

result = re.search("[0-9]*th", "35th")
print(result)
print(result.group())

result = re.search("apple", "this is apple")
print(result)
print(result.group())

result = re.search("\d{4}", "2024 is the year")
print(result)
print(result.group())

