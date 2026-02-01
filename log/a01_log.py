import logging

# logging默认打印Warning级别日志，可设置为INFO级别
# logging.basicConfig(level=logging.INFO)

# 配置其他信息
# filename把日志写入到文件
# filemode='w' 每次都创建一个新文件
logging.basicConfig(level=logging.INFO,
                    format = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                    filename='a01.log',
                    filemode='w')

logging.debug("debug msg")
logging.info("info msg")
logging.warning("warn msg")
logging.error("error msg")
logging.critical("critical msg")

# 记录异常堆栈
try:
    1/0
except:
    logging.exception("除0异常")



