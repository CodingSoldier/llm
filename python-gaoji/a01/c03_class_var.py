class C1:
    # 类变量。python没有静态属性
    num = 1
    def __init__(self, x, y):
        # 实例变量x、y
        self.x = x
        self.y = y

c1 = C1(200, 300)   
c1.num = 11
print(c1.num, c1.x, c1.y)
# 实例变量不会影响类变量
print(C1.num)

# 修改类变量
C1.num = 100

c12 = C1(444, 555)
print(c12.num, c12.x, c12.y)

