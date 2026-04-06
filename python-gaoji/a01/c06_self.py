class Person:
    """
    人
    """
    name = "张三"

class Student(Person):
    def __init__(self, school_name):
        self.school_name = school_name


user = Student("北大")

# 查询类属性
print(user.__dict__)
# 输出 {'school_name': '北大'}  只能输出自己的属性，不包含继承的name属性

# 可以动态添加属性
user.__dict__['addr'] = "北京"
print(user.addr)

# 建议优先使用这种，而不是通过__dict__操作属性
user.teacher = "王五"
print(user.teacher)

# 类也是对象，也有属性
print(Person.__dict__)

a = [1, 2]
print(dir(a))

