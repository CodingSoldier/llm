import time
from concurrent.futures import ProcessPoolExecutor, as_completed


#多进程编程
#耗CPU操作，用多进程。多IO操作，用多线程。进程有自己独立的内存空间，切换进程代价高于多线程


def random_sleep(n):
    time.sleep(n)
    return n

if __name__ == "__main__":
    # 进程池
    with ProcessPoolExecutor(3) as executor:
        all_task = [executor.submit(random_sleep, (num)) for num in [2]*30]
        start_time = time.time()
        for future in as_completed(all_task):
            data = future.result()
            print("exe result: {}".format(data))
        print("last time is: {}".format(time.time() - start_time))




