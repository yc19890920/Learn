"""
给定两个非空链表来表示两个非负整数。位数按照逆序方式存储，它们的每个节点只存储单个数字。将两数相加返回一个新的链表。
你可以假设除了数字 0 之外，这两个数字都不会以零开头。

示例：
输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
输出：7 -> 0 -> 8
原因：342 + 465 = 807
"""


class ListNode:

    def __init__(self, val):
        self.val = val
        self.next = None


def addTwoNumbers(l1: ListNode, l2: ListNode):
    if not l1:
        return l2
    if not l2:
        return l1

    if l1.val + l2.val < 10:
        l3 = ListNode(l1.val + l2.val)
        l3.next = addTwoNumbers(l1.next, l2.next)
    else:
        l3 = ListNode(l1.val + l2.val - 10)
        tmp = ListNode(1)
        tmp.next = None
        l3.next = addTwoNumbers(l1.next, addTwoNumbers(l2.next, tmp))
    return l3


if __name__ == "__main__":
    la = ListNode(2)
    la.next = ListNode(4)
    la.next.next = ListNode(3)

    lb = ListNode(5)
    lb.next = ListNode(6)
    lb.next.next = ListNode(4)

    ss = addTwoNumbers(la, lb)
    print(ss.val)
    print(ss.next.val)
    print(ss.next.next.val)
    print(ss.next.next.next)