class A:
    def __init__(self):
        print("A")


class B(A):
    def __init__(self):
        super().__init__()
        print("B")


class C(A):
    def __init__(self):
        super().__init__()
        print("C")


class D(B, C):
    def __init__(self):
        super(D, self).__init__()
        print("D")

# python需要手动调用父类的构造函数
# A、B、C、D是菱形继承关系，调用父类构造函数的顺序、次数由C3算法确定
print(D.__mro__)
d = D()