import array

# array和list的一个重要区别是array只能存放指定的数据类型
my_array = array.array("i")
my_array.append(1)
print(my_array)
# my_array.append("abc")

