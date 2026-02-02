import time

from loguru import logger
import requests

# 日志添加到a02.log，控制台也会打印日志
# logger.add("./log/a02.log")

logger.add("./log/a02.log",
           level="DEBUG",
           format="{time} - {level} - {message}")

def main():
    # start01()

    # rotating()

    formatting()

def start01():
    logger.debug("debug msg")
    logger.info("info msg")
    logger.warning("warning msg")
    logger.error("error msg")
    logger.critical("critical msg")

    try:
        1/0
    except:
        logger.exception("捕获除0异常")

# 滚动压缩
def rotating():
    # logger.add("./log/a02_{time:YYYY-MM-DD}.log", rotation="1 GB", retention="1 week", compression="zip")  # Automatically rotate too big file
    logger.add("./log/a02_{time:YYYY-MM-DD}.log", rotation="1 MB", retention="1 week", compression="zip")  # Automatically rotate too big file

    url = "https://code.jquery.com/jquery-4.0.0.js"

    # 循环执行一万次
    for i in range(10000):
        response = requests.get(url)
        if response.status_code == 200:
            logger.info(response.text)
        else:
            print(f"第 {i + 1} 次请求失败，状态码: {response.status_code}")
            logger.error(f"第 {i + 1} 次请求失败: {response.status_code}")

# format
def formatting():
    logger.info("If you're using Python {}, prefer {feature} of course!", 3.6, feature="f-strings")


if __name__ == "__main__":
    main()
