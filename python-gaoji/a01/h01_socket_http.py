import socket
from urllib.parse import urlparse


#使用socket实现http请求
def get_url(url):
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 80))

    send_data = "GET {} HTTP/1.1\r\nHost{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8")
    client.send(send_data)

    data = b""
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break

    data = data.decode("utf8")
    print(data)
    html_data = data.split("\r\n\r\n")[1]
    print(html_data)
    client.close()


get_url("http://pypi.org/")










