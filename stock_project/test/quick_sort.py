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