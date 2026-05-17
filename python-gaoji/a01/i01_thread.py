import threading
import time

def get_detail_html(url):
    print("start detail html")
    print(url)
    time.sleep(2)
    print("get detail html end")

def get_detail_url(url):
    print("get detail url started")
    print(url)
    time.sleep(4)
    print("get detail url end")


# 创建线程
thread1 = threading.Thread(target=get_detail_html, args=("thread1",))
thread2 = threading.Thread(target=get_detail_url, args=("thread2",))

thread1.start()
thread2.start()

thread1.join()
thread2.join()