a = {
    "bobby1": {
        "company": "imooc"
    },
    "bobby2": {
        "company": "imooc2"
    }
}

# a.clear()
# print(a)

# # 浅拷贝
# c_dict = a.copy()
# c_dict["bobby1"]["company"]="imooc3"
#
# print(a)
# print(c_dict)


# fromkeys使用给定的键列表创建一个新字典
new_list = ["bobby1", "bobby2"]
new_dict = dict.fromkeys(new_list, {"company":"imooc"})
print(new_dict)








