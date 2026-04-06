import abc

# Python 的 abc 模块（Abstract Base Classes，抽象基类）用于定义抽象基类，它是一种 接口规范机制 ，用于强制子类实现特定的方法。相当于JAVA中的接口、虚拟类

class CacheBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def set(self, key, value):
        pass

class CacheBase2():
    def get(self, key):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

# 使用python的鸭子类型，RedisCache继承CacheBase2，也能实现继承
# 但是RedisCache()不会报错，只有执行到未实现方法才报错
# class RedisCache(CacheBase2):
class RedisCache(CacheBase):
    def set(self, key, value):
        pass
    
    # RedisCache不实现CacheBase的所有方法，RedisCache()时会报错
    def get(self, key):
        pass

redis_cache = RedisCache()
# isinstance用于 检查一个对象是否是指定类或其子类的实例
print(isinstance(redis_cache, RedisCache))
print(isinstance(redis_cache, CacheBase))
redis_cache.set("key1", "value111")
redis_cache.get("key1")

