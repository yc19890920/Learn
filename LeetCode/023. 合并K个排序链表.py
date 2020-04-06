"""
合并 k 个排序链表，返回合并后的排序链表。请分析和描述算法的复杂度。

示例:

输入:
[
  1->4->5,
  1->3->4,
  2->6
]
输出: 1->1->2->3->4->4->5->6
"""

import heapq
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def mergeKLists(self, lists) -> ListNode:
        h = []
        for lst in lists:
            while lst:
                heapq.heappush(h, lst.val)
                lst = lst.next

        cur = ListNode(-1)
        head = cur
        print(h)
        while h:
            smallest = heapq.heappop(h)
            cur.next = ListNode(smallest)
            cur = cur.next
        return head.next



a = ListNode(1)
a.next = ListNode(4)
a.next.next = ListNode(5)

b = ListNode(1)
b.next = ListNode(3)
b.next.next = ListNode(4)

c = ListNode(2)
c.next = ListNode(6)


s = Solution()
res = s.mergeKLists([a,b,c])
while res:
    print(res.val)
    res = res.next
