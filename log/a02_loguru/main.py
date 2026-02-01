import logging

from loguru import logger

# 日志添加到a02.log，控制台也会打印日志
# logger.add("a02.log")

logger.add("a02.log",
           level="DEBUG",
           format="{time} - {level} - {message}")

def main():
    logger.debug("debug msg")
    logger.info("info msg")
    logger.warning("warning msg")
    logger.error("error msg")
    logger.critical("critical msg")

    try:
        1/0
    except:
        logger.exception("捕获除0异常")

if __name__ == "__main__":
    main()
