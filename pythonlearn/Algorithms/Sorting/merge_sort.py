# -*- coding: utf-8 -*-

"""
归并排序原理：
归并排序是基于对两个有序序列进行排序变成新的有序序列的方式进行排序的，假如有两个有序序列，从第一个值开始一个一个比较，
小的就插入到新的序列中，并使得其位置加一，最后，两个序列中会有某一个序列还剩下最大值，将该最大值插入到新的序列中就完成了排序。
归并排序使用递归方式将一个序列从中间分成左右两个序列，再将左右两个序列从中间分成四个序列。
递归下去最后分到每个序列中只有一个元素，将这个元素返回，到上一级调用两序列排序方式，将两个值排序，返回新的排序好的序列，
就这样一层一层递归上来，最后使得序列有序。该方式是使用空间换取排序时间的算法。
归并排序的时间复杂度是O(nlog2n),是一种稳定的算法，逻辑比较复杂

但是归并排序是使用递归实现的，递归次数较多的话，也会影响排序的时间，但是相对于上面的排序算法，该算法的时间消耗将大大缩短。

基本思想：
归并排序是一种典型的分治思想，把一个无序列表一分为二，对每个子序列再一分为二，继续下去，直到无法再进行划分为止。
然后，就开始合并的过程，对每个子序列和另外一个子序列的元素进行比较，依次把小元素放入结果序列中进行合并，最终完成归并排序。
"""

def merge_list(arr1, arr2):
    i, j, T = 0, 0, []
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            T.append(arr1[i])
            i += 1
        else:
            T.append(arr2[j])
            j += 1
    T.extend(arr1[i:])
    T.extend(arr2[j:])
    return T

def merge_sort(arr):
    length = len(arr)
    if length<2: return arr
    arr1 = merge_sort(arr[:length>>1])
    arr2 = merge_sort(arr[length>>1:])
    return merge_list(arr1, arr2)

############################################################
def merge_sort2(arr):
    length = len(arr)
    if length<2: return arr
    T=[]
    arr1 = merge_sort2(arr[:length>>1])
    arr2 = merge_sort2(arr[length>>1:])
    while len(arr1) and len(arr2):
        if arr1[0] <= arr2[0]:
            T.append(arr1.pop(0))
        else:
            T.append(arr2.pop(0))
    if len(arr1):
        T.extend(merge_sort2(arr1))
    if len(arr2):
        T.extend(merge_sort2(arr2))
    return T

############################################################
from collections import deque
def merge_sort3(lst):
    if len(lst) <= 1:
        return lst

    def merge(left, right):
        merged,left,right = deque(),deque(left),deque(right)
        while left and right:
            merged.append(left.popleft() if left[0] <= right[0] else right.popleft())  # deque popleft is also O(1)
        merged.extend(right if right else left)
        return list(merged)

    middle = int(len(lst) // 2)
    left = merge_sort(lst[:middle])
    right = merge_sort(lst[middle:])
    return merge(left, right)





if __name__ == "__main__":
    list1 = [0, 9, 1, 3, 2, 5, 4, 12, 2, 3, 5]
    list1=merge_sort(list1)
    print list1

    list1 = [0, 9, 1, 3, 2, 5, 4, 12, 2, 3, 5]
    list1=merge_sort2(list1)
    print list1

    list1 = [0, 9, 1, 3, 2, 5, 4, 12, 2, 3, 5]
    list1=merge_sort3(list1)
    print list1