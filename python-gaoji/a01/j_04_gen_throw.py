
def gen_func():
    try:
        yield "https://cn.bing.com/"
    except Exception as e:
        pass
    yield 2
    yield 3
    yield 4
    return "bobby"

if __name__ == '__main__':
    gen = gen_func()
    print(next(gen))
    print(gen.throw(Exception, "第1次传入异常"))
    print(next(gen))
    print(gen.throw(Exception, "第2次传入异常"))