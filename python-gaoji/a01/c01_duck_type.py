class Cat:
    def say(self):
        print("I am a cat")

class Dog:
    def say(self):
        print("I am a dog")

class Duck:
    def say(self):
        print("I am a duck")

# 鸭子类型：如果它走起来像鸭子，叫起来像鸭子，那么它就是鸭子。
# 在 Python 中， 鸭子类型 是一种编程风格： 关注对象的行为（方法和属性），而不是对象的类型本身 。
animals = [Cat, Dog, Duck]        
# for循环，不关注animal的类型，只关注animal是否有say方法
for animal in animals:
    animal().say()


a = ["aas", "bbs", "ccc"]
name_set = set()
name_set.add("set111")
name_set.add("set222")
# extend函数的参数是Iterable[_T]类型，只要实现了__iter__ 就能作为extend的入参
a.extend(name_set)
print(a)