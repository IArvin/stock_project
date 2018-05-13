# -*-coding: utf-8-*-
import sys
import os


# def quick_sort(test_list, low, high):
#     if low < high:
#         key_index = sub_sort(test_list, low, high)
#         quick_sort(test_list, low, key_index)
#         quick_sort(test_list, key_index+1, high)
#     return test_list
#
#
# def sub_sort(test_list, low, high):
#     key = test_list[low]
#     while low < high:
#         while low < high and test_list[high] >= key:
#             high -= 1
#         while low < high and test_list[high] < key:
#             test_list[low] = test_list[high]
#             low += 1
#             test_list[high] = test_list[low]
#             test_list[low] = key
#     return low

def quick_sort(test_list, low, high):
    if low < high:
        key_index = sub_sort(test_list, low, high)
        quick_sort(test_list, low, key_index)
        quick_sort(test_list, key_index+1, high)
    return test_list

def sub_sort(test_list, low, high):
    key = test_list[low]
    while low < high:
        while low < high and test_list[high] >= key:
            high -= 1
        while low < high and test_list[high] < key:
            test_list[low] = test_list[high]
            low += 1
            test_list[high] = test_list[low]
            test_list[low] = key
    return low


if __name__ == '__main__1':
    test_list = [8, 10, 9, 6, 4, 16, 5, 13, 26, 18, 2, 45, 34, 23, 1, 7, 3]
    result = quick_sort(test_list, 0, len(test_list)-1)
    print result



def test():
    test_list = [123, -123]
    asd = []
    for a in test_list:
        b = 0
        if a > 0:
            b = int(str(a)[::-1])
        else:
            b = int('-'+str(abs(a))[::-1])
        asd.append(b)
    return asd

result = test()
print result

import xlrd
import xlwt
from xlutils.copy import copy

# 打开想要更改的excel文件
old_excel = xlrd.open_workbook('demo.xls', formatting_info=True)
# 将操作文件对象拷贝，变成可写的workbook对象
new_excel = copy(old_excel)
# 获得第一个sheet的对象
ws = new_excel.get_sheet(0)
# 写入数据
ws.write(0, 0, u'第一行，第一列')
ws.write(0, 1, u'第一行，第二列')
ws.write(0, 2, u'第一行，第三列')
ws.write(1, 0, u'第二行，第一列')
ws.write(1, 1, u'第二行，第二列')
ws.write(1, 2, u'第二行，第三列')
# 另存为excel文件，并将文件命名
new_excel.save('demo.xls')