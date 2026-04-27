# 模式[start:end:step]
"""
    start表示切片开始位置，默认为0
    end表示切片机制（但不包含）位置，默认为列表长度
    step表示切片的步长，默认为1
    
    start=0时，可以省略
    end=列表长度时，可以省略
    step=1时，可以省略，并且省略步长时，同时省略最后一个冒号

    step为负数时，表示反向切片，这时start应该比end的值要大才行
"""
aList = [0, 1, 2, 3, 4, 5, 6]

# 返回包含原列表所有元素的新列表
print(aList[::])

# 逆序列表
print(aList[::-1])

# 指定开始结束位置
print(aList[3:6])

# 隔一个取一个，取偶数位置
print(aList[::2])

# 隔一个取一个，取记数位置
print(aList[1::2])

# 切片结束位置大于列表长度，从列表尾部截断
print(aList[0:100])

# 切片开始位置大于列表长度时，返回空列表
print(aList[100:])

# 在列表尾部增加元素
aList[len(aList):] = [7]
print(aList)

# 在列表原始头部插入元素
aList[:0]=[1,2]
print(aList)

# 在列表中间插入元素
aList[6:6]=[4]
print(aList)

# 替换列表元素
aList[:3]=[1,2]
print(aList)

# 删除元素
del aList[:3]
print(aList)
