# -*- coding: utf-8 -*-

"""
原理
当输入的元素是n个0到k之间的整数时，它的运行时间是Θ(n + k)。计数排序不是比较排序，排序的速度快于任何比较排序算法。
由于用来计数的数组C的长度取决于待排序数组中数据的范围（等于待排序数组的最大值与最小值的差加上1），
这使得计数排序对于数据范围很大的数组，需要大量时间和内存。
例如：
    计数排序是用来排序0到100之间的数字的最好的算法，但是它不适合按字母顺序排序人名。
但是，计数排序可以用在基数排序算法中，能够更有效的排序数据范围很大的数组。

步骤
1. 找出待排序的数组中最大和最小的元素
2. 统计数组中每个值为i的元素出现的次数，存入数组 C 的第 i 项
3. 对所有的计数累加（从C中的第一个元素开始，每一项和前一项相加）
4. 反向填充目标数组：将每个元素i放在新数组的第C(i)项，每放一个元素就将C(i)减去1
"""

def count_sort(lst):
    min = 2147483647
    max = 0
    # 取得最大值和最小值
    for x in lst:
        if x < min:
            min = x
        if x > max:
            max = x
    # 创建数组C
    count = [0] * (max - min +1)
    for index in lst:
        count[index - min] += 1
    index = 0
    # 填值
    for a in range(max - min+1):
        for c in range(count[a]):
            lst[index] = a + min
            index += 1
    return lst

if __name__ == "__main__":
    list1 = [0, 9, 1, 3, 2, 5, 4, 12, 2, 3, 5]
    list1=count_sort(list1)
    print list1