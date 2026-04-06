import contextlib


class WithSample:
    def __enter__(self):
        print("打开资源")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("释放资源")

    def do_something(self):
        print("具体业务")

# 使用 __enter__、__exit__ 函数可以实现try final的功能
with WithSample() as sample:
    sample.do_something()

print("###############")

@contextlib.contextmanager
def file_open(file_name):
    print("file open")
    yield {}
    print("file end")

with file_open("模拟打开文件.txt") as fo:
    print("执行文件处理操作")




