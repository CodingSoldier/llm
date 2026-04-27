int_list = [1, 2, 3, 4, 5]
# 列表推导式
qu_list = [item * item for item in int_list]
print(type(qu_list))
print(qu_list)

int_list = [1,2,-3,4,5]
qu_list = [item if item > 0 else abs(item) for item in int_list]
print(qu_list)

int_list1 = [1, 2]
int_list2 = [3, 4]
qu_list = [(first, second) for first in int_list1 for second in int_list2]
print(qu_list)

my_dict = {
    "key1": "bobby1",
    "key2": "bobby2"
}
# 字典推导式
qu_list = [(key, value) for key, value in my_dict.items()]
print(qu_list)

# 生成器表达式
qu_list2 = list(((key, value) for key, value in my_dict.items()))
print(qu_list2)

int_list = [1, 2, 3, 4, 5]
def process_item(item):
    return str(item)
# 字典推导式
int_dict = {process_item(item):item for item in int_list}    
print(int_dict)
