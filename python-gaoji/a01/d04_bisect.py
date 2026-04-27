import bisect
from collections import deque

# bisect用于二分查找和维护有序序列
inter_list = deque()

bisect.insort(inter_list, 3)
bisect.insort(inter_list, 2)
bisect.insort(inter_list, 5)

print(bisect.bisect_left(inter_list, 3))
print(inter_list)



