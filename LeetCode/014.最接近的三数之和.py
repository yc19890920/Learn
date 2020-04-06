"""
给定一个包括 n 个整数的数组 nums 和 一个目标值 target。找出 nums 中的三个整数，使得它们的和与 target 最接近。返回这三个数的和。假定每组输入只存在唯一答案。

例如，给定数组 nums = [-1，2，1，-4], 和 target = 1.

与 target 最接近的三个数的和为 2. (-1 + 2 + 1 = 2).
"""


class Solution(object):
    def threeSumClosest(self, nums, target):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        n, res, diff = len(nums), None, float('inf')
        nums.sort()
        for i in range(n):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            left, right = i+1, n-1
            while left < right:
                cur = nums[i] + nums[left] + nums[right]
                if cur == target:
                    return target
                elif cur > target:
                    right -= 1
                    if abs(cur-target) < diff:
                        diff = abs(cur-target)
                        res = cur
                    while left < right and nums[right] == nums[right+1]:
                        right -= 1
                else:
                    left += 1
                    if abs(cur-target) < diff:
                        diff = abs(cur-target)
                        res = cur
                    while left < right and nums[left] == nums[left-1]:
                        left += 1
        return res


ret = Solution().threeSumClosest([-1,2,1,-4], 1)
print(ret)