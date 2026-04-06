# python中一切皆对象，函数和类也是对象
# 可以赋值给变量。加入到集合中。作为函数的参数、返回值

# 函数赋值给变量
def ask(name="askkkkk"):
    print(name)

# my_func = ask
# my_func("函数赋值给变量")
#
# 类赋值给变量
class Pereson:
    def __init__(self):
        print("实例初始化")

# my_class = Pereson
# my_class()

# # 函数、类 加入到集合中
# # 函数、类 可以作为函数参数
# my_list = []
# my_list.append(ask)
# my_list.append(Pereson)
# for item in my_list:
#     print(item())

# 函数作为返回值
def decorator_func():
    print("函数执行")
    return ask
decorator_func()("函数可以作为返回值")
