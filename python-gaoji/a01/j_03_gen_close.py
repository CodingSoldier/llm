
def gen_func():
    try:
        yield "https://cn.bing.com/"
    except BaseException:
        pass
    yield 2
    yield 3
    return "bobby"

if __name__ == '__main__':
    gen = gen_func()
    print(next(gen))
    # 关闭生成器
    # 由于生成器已经关闭了，gen_func函数yield 2的时候会报错
    gen.close()
    print("end")
