# demoTupleSet.py

# Set 형식 연습
a={1,2,3,3}
b={3,4,4,5}

print(a)
print(b)
print(type(a))
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))

# Tuple 연습
tp = (10,20,30)
print(len(tp))
print(tp.index(20))
print(tp.count(10))

#함수를 정의
def calc(a,b):
    return a+b, a*b

#함수호출
resurt = calc(3,4)
print(type(resurt))
print(resurt)

#일괄입력
print("id:%s, name:%s" % ("kim", "김유신"))

args = (5,6)
print(calc(*args))

#형식변환(Type Casting)
a = set((1,2,3))
print(a)
b = list(a)
b.append(10)
print(b)