class Solution:
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        LEFT = {'(', '[', '{'}  # 左括号
        RIGHT = {')', ']', '}'}  # 右括号
        stack = []  # 创建一个栈
        for i in s:  # 迭代传过来的所有字符串
            if i in LEFT:  # 如果当前字符在左括号内
                stack.append(i)  # 把当前左括号入栈
            elif i in RIGHT:  # 如果是右括号
                if not stack:
                    return False
                tmp = stack.pop()  # 删除左括号
                if i == ')' and tmp != '(':
                    return False
                if i == '}' and tmp != '{':
                    return False
                if i == ']' and tmp != '[':
                    return False
        return not stack  # 如果栈内没有值则返回True，否则返回False


s = Solution()
print(s.isValid("([[])[]{}"))
print(s.isValid("([])[]{[{}]}"))

print(ord("[")-ord("]"))
print(ord("{")-ord("}"))
print(ord("(")-ord(")"))