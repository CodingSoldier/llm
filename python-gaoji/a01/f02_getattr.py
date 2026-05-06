# 访问属性时优先访问__getattribute__
# 属性不存在时访问__getattr__
class User:
    def __init__(self, info=None):
        self.info = {} if info is None else info

    def __getattr__(self, item):
        return self.info[item]

    # def __getattribute__(self, item):
    #     return "优先访问"

user = User(info={"company_name": "imooc", "name": "bobby"})
print(user.test)