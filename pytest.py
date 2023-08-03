import matplotlib.pyplot as plt
from tqdm import tqdm
import time

tot_sum = 0
a = range(10)
for i in tqdm(a):
    time.sleep(0.1)
    tot_sum += i

print(tot_sum)