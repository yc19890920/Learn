""" 实现有序的多重集合（包）
创建一个二叉搜索树（binary search tree）结构用来让所有的元数据都按正确的顺序存储。
1. 设计一个基本的二叉树结构。
2. 决定使用collections.abc.MutableSequence、collections.abc.MutableMapping还是collections.abc.MutableSet作为基类
3. 了解collections.abc的集合中有哪些特殊方法。

一个二叉树搜索的节点有两个分支：一个是“小于”分支，用于存放所有小于当前节点的键；另一个是“大于等于”分支，用于存放所有大于等于当前节点的键


设计原则：
两个类：TreeNode, Tree, TreeNode类包含有的元素和more、less和parent引用。
搜索元素： __contains__(),discard(); 递归
1. 若目标元素和当前元素相同，返回self;
2. 若目标元素比当前元素小，递归使用less.find()继续递归搜素
3. 若目标元素比当前元素大，递归使用more.find()继续递归搜素

Tree 使用外观模式（Facade）也被称为包装模式（Wrapper），
"""
import weakref
import collections.abc

class TreeNode(object):

    def __init__(self, item, less=None, more=None, parent=None):
        self.item = item
        self.less = less
        self.more = more
        if parent is not None:
            self.parent = parent

    @property
    def parent(self):
        return self.parent_ref()

    @parent.setter
    def parent(self, value):
        self.parent_ref = weakref.ref(value)

    def __repr__(self):
        return "TreeNode({item!r}, {less!r}, {more!r})".format(**self.__dict__)

    def find(self, item):
        if self.item is None: # Root
            if self.more:
                return self.more.find(item)
        elif self.item==item:
            return self
        elif self.item>item and self.less:
            return self.less.find(item)
        elif self.item<item and self.more:
            return self.more.find(item)
        raise KeyError

    def __iter__(self):
        if self.less:
            for item in iter(self.less):
                yield item
        yield self.item
        if self.more:
            for item in iter(self.more):
                yield item

    def add(self, item):
        if self.item is None: # Root Special Case
            if self.more:
                self.more.add(item)
            else:
                self.more = TreeNode(item, parent=self)
        elif self.item>item:
            if self.less:
                self.less.add(item)
            else:
                self.less = TreeNode(item, parent=self)
        elif self.item<item:
            if self.more:
                self.more.add(item)
            else:
                self.more = TreeNode(item, parent=self)

    def remove(self, item):
        """
        1. 当删除一个没有孩子的节点时，可以简单的删除，然后将与父节点的引用改为None.
        2. 当删除一个有孩子的节点时，可以用这个孩子代替当前节点在父节点的引用。
        3. 当有两个孩子时，需要调树的结构。首先找到后继节点， 可以利用这个后继节点的值替换准备删除的节点。然后可以删除和之前那个重复的后继几点。
        """
        # Recursive search for node
        if self.item is None or item>self.item:
            if self.more:
                self.more.remove(item)
            else:
                raise KeyError
        elif item < self.item:
            if self.less:
                self.less.remove(item)
            else:
                raise KeyError
        else:
            if self.less and self.more: # Two Children are present
                successor = self.more._least()
                self.item = successor.item
                successor.remove(successor.item)
            elif self.less: # One child on less
                self._replace(self.less)
            elif self.more: # One child on more
                self._replace(self.more)
            else: # Zero children
                self._replace()

    def _least(self):
        """ 在一棵给定的树中查询出最小节点 """
        if self.less is None:
            return self
        return self.less._least()

    def _replace(self, new=None):
        """ 检查父节点，已确定是否需要更新less或者more属性 """
        if self.parent:
            if self == self.parent.less:
                self.parent.less = new
            else:
                self.parent.more = new
        if new is not None:
            new.parent = self.parent

class Tree(collections.abc.MutableSet):

    def __init__(self, itrerable=None):
        self.root = TreeNode(None)
        self.size = 0
        if itrerable:
            for item in itrerable:
                self.root.add(item)

    def add(self, value):
        self.root.add(value)
        self.size += 1

    def discard(self, value):
        try:
            self.root.remove(value)
        except KeyError:
            pass

    def __contains__(self, item):
        try:
            self.root.more.find(item)
            return True
        except KeyError:
            return False

    def __iter__(self):
        for item in iter(self.root.more):
            yield item

    def __len__(self):
        return self.size



s = TreeNode(["Item 1", "Anohter", "Middle"])
print(s)

# s.add("abc")
# print(s)


