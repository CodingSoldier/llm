# 我们需要一个可以暂停的函数，并且可以在适当的时候恢复该函数的继续执行
# 出现了协程 -> 可以暂停的函数（可以向暂停的地方传入值）

# 生成器不只可以产出值，还可以接收值
def gen_func():
    #  yield xxx 产出值
    # html = yield xxx 可以接收值，把值存储到html变量中
    html = yield "https://cn.bing.com/"
    print(html)
    return "end"

if __name__ == '__main__':
    gen = gen_func()
    # 在调用send发送非none值之前，必须启动一次生成器
    # 方式有两种：gen.send(None)、next(gen)
    url = gen.send(None)
    print(url)

    # send方法可以传递值进入生成器内部，同时还可以重启生成器执行到下一个yield位置
    gen.send("test1111")
