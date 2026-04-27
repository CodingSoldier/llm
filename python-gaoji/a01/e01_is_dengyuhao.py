# ==：比较两个对象的值（内容）是否相等
# is：比较两个对象是否是同一个对象（内存地址相同）

a = [1, 2, 3]
b = [1, 2, 3]
c = a
print(a == b)  # True  - 值相同
print(a is b)  # False - 不同的对象，内存地址不同
print(a is c)  # True  - 同一个对象，内存地址相同

print("##############")

# 字符串示例（注意小整数和短字符串的缓存机制）
x = "hello"
y = "hello"
z = "".join(["h", "e", "l", "l", "o"])
print(x == y)  # True
print(x is y)  # True  （Python 会缓存短字符串，可能指向同一对象）
print(x == z)  # True
print(x is z)  # False （动态生成的字符串，不同对象）

print("@@@@@@@@@@@@@@@")
# 整数示例
m = 256
n = 256
p = 257
q = 257

# True  （-5 到 256 的小整数会被缓存）
print(m is n)

# 不要依赖 is 来比较整数值！这种行为是不可靠的
# is 只应用于与单例对象比较（None、True、False）
# 比较整数值时，始终使用 ==
print(p is q)

# True  （但值相等）
print(p == q)



print("*******************")
value = None
if value is None:      # 推荐写法
    print("is none")
