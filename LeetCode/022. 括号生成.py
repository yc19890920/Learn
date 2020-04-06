"""
给出 n 代表生成括号的对数，请你写出一个函数，使其能够生成所有可能的并且有效的括号组合。

例如，给出 n = 3，生成结果为：

[
  "((()))",
  "(()())",
  "(())()",
  "()(())",
  "()()()"
]
"""


class Solution:
    def generateParenthesis(self, n):
        self.res = []
        self.lookup('', 0, 0, n)
        return self.res

    def lookup(self, s, left, right, n):
        if left == n and right == n:
            self.res.append(s)
        if left < n:
            self.lookup(s + '(', left + 1, right, n)
        if right < left:
            self.lookup(s + ')', left, right + 1, n)
