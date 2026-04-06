a = [1, 2]
c = a + [3, 4]  # 不能加元组
print(c)

# 就地加。可以加列表、元组。
# a += (3, 4)
# print(a)

# a.extend(range(10))
# print(a)

# 把整个(1, 3)作为一个元素加到a中
a.append((1, 3))
print(a)