import threading
from threading import Lock

total = 0
# lock = Lock() # 锁
lock = threading.RLock() # 可重入锁

def add():
    global lock
    global total
    for i in range(10000):
        lock.acquire()  # 加上锁。可重入锁可多次加锁
        lock.acquire()  # 加上锁。可重入锁可多次加锁
        total += 1
        lock.release()  # 释放锁
        lock.release()  # 释放锁

def desc():
    global lock
    global total
    for i in range(10000):
        lock.acquire()
        total -= 1
        lock.release()

thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)
thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(total)

# 锁会引起死锁
"""
相互等待锁导致死锁
A(a, b)
acquire(a)
acquire(b)

B(a, b)
acquire(b)
acquire(a)
"""



