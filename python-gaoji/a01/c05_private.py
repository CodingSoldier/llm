from c04_method import Date
class User:
    def __init__(self, birthday):
        # __开头表示私有属性
        self.__birthday = birthday

    def get_age(self):
        return 2026 - self.__birthday.year        

user = User(Date(1990, 2, 1))
print(user.get_age())

# 无法直接获取私有属性
# print(user.__birthday)

# 可以在私有属性前加上_User获取私有属性
print(user._User__birthday)