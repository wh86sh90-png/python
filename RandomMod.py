import random

print(random.random()) # 0.0 ~ 1.0 미만의 실수 난수 생성
print(random.randint(1, 10))    # 1 ~ 10 사이의 정수 난수 생성 (10 포함)
print(random.choice(['가위', '바위', '보']))  # 리스트에서 무작위로 하나 선택
print(random.sample(range(1, 46), 6))  # 1 ~ 45 사이의 숫자 중에서 6개를 무작위로 선택