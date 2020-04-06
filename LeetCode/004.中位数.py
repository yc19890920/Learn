"""
给定两个大小为 m 和 n 的有序数组 nums1 和 nums2。

请你找出这两个有序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。

你可以假设 nums1 和 nums2 不会同时为空。

示例 1:

nums1 = [1, 3]
nums2 = [2]

则中位数是 2.0
示例 2:

nums1 = [1, 2]
nums2 = [3, 4]

则中位数是 (2 + 3)/2 = 2.5
"""
from math import floor


def findMedianSortedArrays(nums1, nums2):
    n = len(nums1) + len(nums2)
    if n == 0:
        return None
    if n % 2 == 1:
        return findKth(nums1, nums2, floor(n / 2) + 1)
    else:
        smaller = findKth(nums1, nums2, floor(n / 2))
        bigger = findKth(nums1, nums2, floor(n / 2) + 1)
        return (smaller + bigger) / 2.0


def findKth(A, B, k):
    if len(A) == 0:
        return B[k - 1]
    if len(B) == 0:
        return A[k - 1]
    if k == 1:
        return min(A[0], B[0])
    a = A[floor(k / 2) - 1] if len(A) >= k / 2 else None
    b = B[floor(k / 2) - 1] if len(B) >= k / 2 else None
    if b is None or (a is not None and a < b):
        return findKth(A[floor(k / 2):], B, k - floor(k / 2))
    else:
        return findKth(A, B[floor(k / 2):], k - floor(k / 2))


if __name__ == "__main__":
    nums1 = []
    nums2 = [2]
    ret = findMedianSortedArrays(nums1, nums2)
    print(ret)

    nums1 = []
    nums2 = []
    ret = findMedianSortedArrays(nums1, nums2)
    print(ret)
