a = 1
print(type(1))
print(type(int))
print(type(type))

s = "sss"
print(type(s))
print(type(str))

class Student:
    pass

stu = Student()
print(type(stu))
print(type(Student))

l = [1, 2]
print(type(l))
print(type(list))

print(Student.__bases__)
print(type.__bases__)
print(object.__bases__)

# 在 Python 中，整数、字符串、列表、类等一切皆对象
# 所有类都继承自object
# 所有类（int、str、Student 等）本身的类型都是type
# type是类，继承自object，type又是创建类的类