import threading
import time
from queue import Queue


def get_detail_html(queue):
    while True:
        url = queue.get()
        print("@@@@@ get detail html = {}".format(url))
        time.sleep(1)

def get_detail_url(queue):
    while True:
        time.sleep(2)
        for i in range(20):
            format_url = "http://projectsedu.com/{id}".format(id=i)
            queue.put(format_url)
            print("put detail url = {}".format(format_url))


# queue是线程安全的的，使用queue作为共享变量，进行多线程通信
detail_url_queue = Queue(maxsize=1000)
detail_thread = threading.Thread(target=get_detail_url, args=(detail_url_queue,))

for i in range(10):
    html_thread = threading.Thread(target=get_detail_html, args=(detail_url_queue,))
    html_thread.start()

detail_thread.start()


