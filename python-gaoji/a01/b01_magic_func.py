class Company(object):
    def __init__(self, employee_list):
        self.employees = employee_list

    def __getitem__(self, item):
        return self.employees[item]

company = Company(["baobo", "tom", "ah"])

# python内置的__XXX__函数叫做魔法函数
# 类实现了__iter__(self)或__getitem__就具备了迭代功能
# python解释器遇到for in，回去找__iter__(self)或__getitem__函数
for item in company:
    print(item)