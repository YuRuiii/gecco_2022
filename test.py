from multiprocessing import Pool, cpu_count
import time

def random_calculation(x):
    while True:
        x * x

p = Pool(processes=cpu_count())
p.map(random_calculation, range(cpu_count()))