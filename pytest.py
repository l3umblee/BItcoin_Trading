import sys, os
sys.path.append(os.pardir)
import matplotlib.pyplot as plt
import time
import schedule
from tc_lib.common import *

def job():
    # 리턴 값이 있는 작업 예시
    result = 10 + 20
    return result

# 시작 시간을 기록합니다.
start_time = time.time()

while True:

    print(job())
    # 총 15분이 경과하면 종료합니다.
    elapsed_time = time.time() - start_time
    if elapsed_time >= 3 * 60:  # 15분은 15 * 60초로 계산합니다.
        print("15 minutes have passed. Exiting the program.")
        break

    time.sleep(60)