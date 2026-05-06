# 类也是对象
# type是创建类的类
from collections import Counter


def create_class(name):
    if name == "user":
        class User:
            def __str__(self):
                return "user"
        return User
    elif name == "company":
        class Company:
            def __str__(self):
                return "company"
        return Company

MyClass = create_class("user")
my_obj = MyClass()
print(type(my_obj))


class MetaClass(type):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

class User(metaclass=MetaClass):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "user"

my_user = User(name="bobby")
print(my_user)

