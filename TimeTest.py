

import time

# print(time.time())

# time.sleep(10)
# print(time.gmtime())
# print(time.localtime())

import datetime

d1 = datetime.datetime.today()
print(d1)
d2 = datetime.datetime.now()
print(d2)
d3 = datetime.date(2025, 12, 25)
print(d3)

# 날짜 간격 계산
d4 = datetime.timedelta(days=100)
print(d1 + d4)