import threading


class TianMao(threading.Thread):
    def __init__(self, cond):
        super().__init__(name="天猫精灵")
        self.cond = cond

    def run(self):
        with self.cond:
            print("{} : 小爱同学".format(self.name))
            self.cond.notify()
            self.cond.wait()

            print("{}：我们来对古诗吧。".format(self.name))
            self.cond.notify()
            self.cond.wait()


class XiaoAi(threading.Thread):
    def __init__(self, cond):
        super().__init__(name="小爱同学")
        self.cond = cond

    def run(self):
        with self.cond:
            self.cond.wait()
            print("{} : 我在".format(self.name))
            self.cond.notify()

            self.cond.wait()
            print("{}：好的。".format(self.name))
            self.cond.notify()

# Condition 条件变量，用与复杂的线程间同步
cond = threading.Condition()
xiaoAi = XiaoAi(cond)
tianmao = TianMao(cond)

xiaoAi.start()
tianmao.start()