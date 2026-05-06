import numbers


# 数据描述符
class IntField:
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError("int value need")
        if value < 0:
            raise ValueError("positive value need")
        self.value = value
    def __delete__(self, instance):
        pass

# 非数据描述符
class NonDataIntField:
    def __get__(self, instance, owner):
        return self.value

class User:
    # 会走__set__方法
    # age = IntField()

    # 只有__get__方法，不会出发__set__方法的校验
    age = NonDataIntField()


user = User()
user.__dict__["age"] = "afdf"
print(user.__dict__)
print(user.age)