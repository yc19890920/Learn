# -*- coding: utf-8 -*-

"""
堆排序使用的是堆这种数据结构，我们这里用列表才存储堆。
核心思想：
    先建立一个最大堆，在建立最大堆的过程中需要不断调整元素的位置。最大堆建立后，顶端元素必定是最大的元素，
    把该最大元素与最末尾元素位置置换，最大元素就出现在列表末端。重复此过程，直到排序。


堆排序是对选择排序的一种优化算法，都属于选择排序类。
基本过程：
    堆是一种完全二叉树，是一种树形选择结构，将待排序的序列构造成一个大顶堆(即每个节点的值都大于或等于其左右孩子节点的值)，
然后将堆顶的根节点移走，与堆数组的末尾元素交换，此时末尾元素就是最大值。
再将剩余的n-1个序列重新构造一个堆，得到次大值置于末尾，反复执行得到一个有序序列。
这里需要注意的，堆排序为了方便完全二叉树的计数，序列的首位置为空，忽略不计。



堆的特点就是FIFO(first in first out)先进先出，这里的话我觉得可以理解成树的结构。堆在接收数据的时候先接收的数据会被先弹出。
栈的特性正好与堆相反，是属于FILO(first in/last out)先进后出的类型。栈处于一级缓存而堆处于二级缓存中。这个不是本文重点所以不做过多展开。

"""

import heapq

############################################################
def heap_sort3(lst):
    n = len(lst)-1              # 这里注意根据python的range列表的性质，要将序列长度减一，否则列表长度溢出
    for i in range(n/2, 0, -1):
        heap_adjust(lst, i, len(lst))

    while n > 1:
        lst[1], lst[n] = lst[n], lst[1]   # 将堆顶记录和当前未经排序子序列的最后一个记录交换
        heap_adjust(lst, 1, n)            # 将lst[n]重新调整为大顶堆
        n -= 1
    return lst[1:]                      # 这里为了方便完全二叉树的计数，将序列中的首个元素置为空忽略不计

def heap_adjust(lst, k, size):      # 自顶向下堆化，从k开始堆化
    N = size - 1
    while 2 * k <= N:
        lchild = 2 * k
        rchild = 2 * k + 1
        if lchild < N and lst[lchild] < lst[rchild]:  # 选出左右孩子节点中更大的那个，并将关键字赋值给左孩子
            lchild = rchild
        if lst[k] < lst[lchild]:                      # 将左孩子与父节点比较，选出大的
            lst[k], lst[lchild] = lst[lchild], lst[k]
            k = lchild              # 将k扩倍，对孙节点排序
        else:
            break


##############################################
"""
堆排序（Heapsort）是指利用堆这种数据结构所设计的一种排序算法。
堆是一个近似完全二叉树的结构，并同时满足堆积的性质：即子结点的键值或索引总是小于（或者大于）它的父节点。
步骤
1. 创建最大堆:将堆所有数据重新排序，使其成为最大堆
2. 最大堆调整:作用是保持最大堆的性质，是创建最大堆的核心子程序
3. 堆排序:移除位在第一个数据的根节点，并做最大堆调整的递归运算
"""
def heap_sort4(arr):
    length = len(arr)
    # 创建最大堆
    for start in range(length - 2 // 2, -1, -1):
        sift_down(arr, start, length - 1)
    # print '----------', arr

    # 堆排序
    for end in range(length - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(arr, 0, end - 1)
    return arr

# 最大堆调整
def sift_down(arr, start, end):
    root = start
    while True:
        child = 2 * root + 1
        if child > end:
            break
        if child + 1 <= end and arr[child] < arr[child + 1]:
            child += 1
        if arr[root] < arr[child]:
            arr[root], arr[child] = arr[child], arr[root]
            root = child
        else:
            break

##############################################
# 利用 heap 排序
def heap_sort(arr):
    heapq.heapify(arr)
    T = heapq.nsmallest(len(arr), arr)
    return T


##############################################
# 堆排序
def heapq_sort5(arr):
    T = []
    map(lambda v: heapq.heappush(T, v), arr)
    return [heapq.heappop(T) for _ in xrange(len(T))]


##############################################
def main1():
    list1 = [0, 9, 1, 3, 2, 5, 4, 12, 2, 3, 5, 1000, 200]
    lst=heap_sort(list1)
    # print lst

def main2():
    list1 = [0, 9, 1, 3, 2, 5, 4, 12, 2, 3, 5, 1000, 200]
    lst5 = heapq_sort5(list1)
    # print lst5

def main3():
    list1 = [0, 9, 1, 3, 2, 5, 4, 12, 2, 3, 5, 1000, 200]
    lst = heap_sort4(list1)
    # print lst

if __name__ == "__main__":
    import timeit
    print timeit.timeit("main1()", setup="from __main__ import main1", number=10000)

    print timeit.timeit("main2()", setup="from __main__ import main2", number=10000)

    print timeit.timeit("main3()", setup="from __main__ import main3", number=10000)



