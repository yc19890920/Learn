"""
3. 无重复字符的最长子串
给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。
示例 1:
输入: "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3

示例 2:
输入: "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。

示例 3:
输入: "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
"""

def longest_substring(s):
    """
    程序变量解释
    l(字母L) 代表目前最大子串的长度
    start 是这一轮未重复子串首字母的index
    maps 放置每一个字符的index，如果maps.get(s[i], -1)大于等于start的话，就说明字符重复了，此时就要重置 l(字母L) 和start的值了，
    """
    l, start, n = 0, 0, len(s)
    maps = {}
    for i in range(n):
        start = max(start, maps.get(s[i], -1) + 1)
        l = max(l, i - start + 1)
        maps[s[i]] = i
    print(start)
    return l


if __name__ == "__main__":
    s = "123456qwerqwertyui"
    ret = longest_substring(s)
    print(ret)