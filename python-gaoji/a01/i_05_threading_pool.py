import time
from asyncio import ALL_COMPLETED
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED


# 线程池，为什么要用线程池
# 主线程中可以获取某一个线程状态或者某一个任务的状态，以及返回值
# 当一个线程完成的时候，我们主线程能立刻知道
# futures可以让多线程和多进程编码接口一致

def get_html(times):
    time.sleep(times)
    print("get page {} success.".format(times))
    return times

executor = ThreadPoolExecutor(max_workers=2)

# task1 = executor.submit(get_html, (3))
# task2 = executor.submit(get_html, (2))
#
# # done用于判断某个任务是否完成
# print(task1.done())
# time.sleep(3)
# print(task1.done())
#
# # result可以获取task的执行结果
# print(task1.result())


ts = [3, 2, 4]
all_task = [executor.submit(get_html, (t)) for t in ts]

# # 等待所有线程执行完成
# wait(all_task, return_when=ALL_COMPLETED)

# # as_completed按完成顺序返回future对象
# for future in as_completed(all_task):
#     data = future.result()
#     print("get {} page".format(data))

for data in executor.map(get_html, ts):
    print("get {} page".format(data))

print("main")



