
class User:
    def __new__(cls, *args, **kwargs):
        print("in new")
        return super().__new__(cls)

    def __init__(self, name):
        print("in init")
        self.name = name

# new 用来控制对象的生成过程，在对象生成之前调用
# 如果new方法不返回对象，则不会调用init函数
# init 用来完善对象
user = User(name = "bobby")

