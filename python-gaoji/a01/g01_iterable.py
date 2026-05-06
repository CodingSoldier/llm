# 迭代器是访问集合元素的一种方式，一般用来遍历数据
# 迭代器和下标访问方式不一样：
#   - 下标访问可以随机访问任意位置
#   - 迭代器只能从头到尾逐个访问，不能回退
# 迭代器提供了一种惰性访问数据的方式，节省内存
from collections.abc import Iterator


class MyInterator(Iterator):
    def __init__(self, employee_list):
        self.employee_list = employee_list
        self.index = 0

    def __next__(self):
        # 返回迭代值
        try:
            word = self.employee_list[self.index]
        except IndexError:
            raise StopIteration
        self.index = self.index + 1
        return word

class Company:
    def __init__(self, employee_list):
        self.employee_list = employee_list

    def __iter__(self):
        return MyInterator(self.employee_list)

company = Company(["tom", "bob", "jane"])

for item in company:
    print(item)