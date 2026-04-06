class Date:

    # 构造方法
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # 实例方法
    def tomorrow(self):
        self.day += 1

    # 静态方法
    @staticmethod
    def parse_string1(date_str):
        year, month, day = tuple(date_str.split("-"))
        return Date(int(year), int(month), int(day))

    # 类方法
    # 相比与静态方法，类方法可以接收cls作为入参，修改类名时，不用像静态方法那样修改Date类名
    @classmethod
    def parse_string2(cls, date_str):
        year, month, day = tuple(date_str.split("-"))
        return cls(int(year), int(month), int(day))

    def __str__(self):
        return "{year}/{month}/{day}".format(year=self.year, month=self.month, day=self.day)


day = Date(2026, 4, 5)
print(day)

day.tomorrow()
print(day)

d1 = Date.parse_string1("2026-04-05")
print(d1)

d2 = Date.parse_string2("2026-04-05")
print(d2)
