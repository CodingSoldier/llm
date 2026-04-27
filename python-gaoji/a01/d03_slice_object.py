import numbers

class Group:
    def __init__(self, group_name, company_name, staffs):
        self.group_name = group_name
        self.company_name = company_name
        self.staffs = staffs

    def __getitem__(self, item):
        cls = type(self)
        if isinstance(item, slice):
            return cls(group_name=self.group_name, company_name=self.company_name, staffs=self.staffs[item])
        if isinstance(item, numbers.Integral):
            return cls(group_name=self.group_name, company_name=self.company_name, staffs=[self.staffs[item]])
    
    def __iter__(self):
        return iter(self.staffs)

    def __repr__(self):
        return f"Group(group_name='{self.group_name}', company_name='{self.company_name}', staffs={self.staffs})"


staffs = ["a1", "a2", "a3", "a4"]
group = Group(group_name="分组1", company_name="公司1", staffs=staffs)

# 实现__getitem__(self, item)方法，即可使用切片
sub_group = group[:3]
print(sub_group)
elem1 = group[0]
print(elem1)

# 实现 __iter__(self) 方法，即可使用for迭代语法
for e in group:
    print(e)