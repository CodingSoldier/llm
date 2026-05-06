# 函数有yield关键字，就是生成器函数
def gen_func():
    yield 1
    yield 2
    yield 3

# 使用生成器实现斐波那契数列
def gen_fib(index):
    n,a,b = 0,0,1
    while n<index:
        yield b
        a,b = b, a+b
        n += 1

# gen = gen_func()
# for value in gen:
#     print(value)

for value in gen_fib(10):
    print(value)