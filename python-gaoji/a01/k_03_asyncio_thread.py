import asyncio
import time
import socket
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

def get_url(url):
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 80)) #阻塞不会消耗cpu

    client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8"))

    data = b""
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break

    data = data.decode("utf8")
    html_data = data.split("\r\n\r\n")[1]
    print(html_data)
    client.close()

# 在协程中使用线程运行阻塞任务
async def async_func():
    start_time = time.time()
    with ThreadPoolExecutor(3) as executor:
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(executor, get_url, f"https://cn.bing.com/{i}/") for i in range(20)
        ]
        await asyncio.gather(*tasks)
        print(f"last time:{time.time() - start_time}")

if __name__ == '__main__':
    asyncio.run(async_func())


