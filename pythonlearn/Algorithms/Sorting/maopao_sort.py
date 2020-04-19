# -*- coding: utf-8 -*-

"""
冒泡排序原理：
从左到右先找第一个值，然后拿这个值右边的值和它进行比较，假如右边的值比它小，那就将右边的这个值和它进行交换，
这样，就能够将整个列表中最小的值放到最左边，第一次排序完成，之后对第二个数也进行相同的操作，最终整个列表变成有序的。

冒泡排序法的时间复杂度是O(n**2),是一种稳定排序算法，逻辑比较简单。

"""
def maopao_sort1(arr):
    length = len(arr)
    for i in xrange(length):
        for j in xrange(length-i-1):
            if arr[j] > arr[j+1]:
                arr[j+1], arr[j] = arr[j], arr[j+1]

def maopao_sort2(arr):
    length = len(arr)
    for i in xrange(length):
        for j in xrange(i, length):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]


# 冒泡排序改进 双向排序
"""
冒泡双向排序的原理：
冒泡排序的改进其实就是在对第一个值寻找最小值的同时也在对最后一个值寻找最大值，双向寻找，
这样，一次排序下来，能得到左右两边两个排好序的值，这样，总的执行排序的次数将减少一半。
但是，在python中，双向排序的使用时间和冒泡排序使用的时间差不多，并没有将时间减半，
这应该是由于python中list的实现方式的关系，python中的list内部实现机制其实还是数组，只不过数组里面还加了一块缓存空间，
这样移动某一个元素，其他的元素也需要移动。所以并没有达到优化冒泡排序的目的（PS:原因分析是基于我自己的理解，可能有不对之处。。。）

双向排序的时间复杂度是O(N**2)，是一种稳定排序算法，逻辑比较简单
"""

def maopao_optimize_sort(arr):
    length = len(arr)
    midle_index = length>>1
    for i in xrange(midle_index):
        for j in range(i, length-i-1):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
            if arr[j] > arr[-i-1]:
                arr[j], arr[-i-1] = arr[-i-1], arr[j]


if __name__ == "__main__":
    list1 = [1, 3, 2, 5, 4]
    maopao_sort1(list1)
    print list1

    list2 = [1, 3, 2, 5, 4]
    maopao_sort2(list2)
    print list2

    list3 = [1, 3, 2, 5, 4]
    maopao_optimize_sort(list3)
    print list3

