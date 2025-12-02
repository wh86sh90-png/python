# Function_1.py

#1 함수 정의
def setValue(newValue):
    x=newValue
    print("함수내부:", x)

def swap(x,y):
    return y,x

def times(a=10, b=20):
    return a*b

def connectURI(server, port):
    strURL="https://" + server + ":" + port
    return strURL

def union(*ar):
    #지역변수
    result = []
    for item in ar:
        for x in item:
            if x not in result:
                result.append(x)
    return result

#2 함수 호출
result = setValue(5)
print(result)

result = swap(3,4)
print(result)

print("---기본값을 명시")
print(times())
print(times(5))
print(times(5,6))

print("---키워드 인자---")
print(connectURI("naver.com", "80"))
print(connectURI(port="8080", server="naver.com"))
print(dir())
print(globals())

print("---가변인자---")
print(union("HAM", "EGG"))
print(union("HAM", "EGG", "SPAM"))