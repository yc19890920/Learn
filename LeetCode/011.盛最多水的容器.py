from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        area = 0
        while left < right:
            cur = min(height[left], height[right]) * (right - left)
            area = max(area, cur)
            # 较短的垂直线往中间走
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return area


ret = Solution().maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7])

print(ret)
# 49
