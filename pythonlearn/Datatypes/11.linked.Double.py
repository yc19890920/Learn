# -*- coding: utf-8 -*-

'''
双向链表
链表L中的每个元素都是一个对象，每个对象有一个关键字key和两个指针：next和prev，对象中还可以包含其他辅助数据（卫星数据）。
若x是链表中的一个元素，则有：
    x.next指向它在链表中的后继元素，x.prev指向它的前驱元素
    若x.prev = None，则元素x是链表的第一个元素，即链表的头(head)
    若x.next = None, 则元素x是链表的最后一个元素，即链表的尾(tail)
    L.head指向链表L的第一个元素，若L.head = None，则链表为空。

简化操作：哨兵
哨兵L.nil是一个哑对象，表示None，其作用是简化边界条件的处理。
将常规的双向链表转变为一个有哨兵的双向循环链表：
    哨兵L.nil位于表头和表尾之间
    属性L.nil.next指向表头，L.nil.prev指向表尾
    表尾的next属性和表头的prev属性同时指向L.nil
    把对L.head的引用代替为对L.nil.next的引用
    一个空的链表只由一个哨兵构成，L.nil.next和L.nil.prev同时指向L.nil

注意：仅当真正简化代码时才使用哨兵。
'''

# 节点
class DNode(object):
    def __init__(self, value=0, prev=None, next=None):
        self.value = value
        self.next = next
        self.prev = prev

# 双向循环列表（无哨兵）
class DLink(object):

    def __init__(self):
        self.head = None #表头初始为None

    def search(self, key):
        '''
        返回指向第一个关键字为key的元素的指针
        若无关键字为k的对象，则返回None
        '''
        x = self.head
        while x is not None  and x.value != key :
            x = x.next
        return x

    def insert(self, x):
        '''
        x为已设置好关键字key的元素
        将x插入到链表的前端
        '''
        x.next = self.head
        if self.head is not None:
            self.head.pre = x
        self.head = x
        x.pre = None

    def delete(self, x):
        '''删除元素'''
        if not isinstance(x, DNode): x = self.search(x)
        if x is None: return
        if x.prev is not None: # x不是第一个结点
            x.pre.next = x.next
        else:
            self.head = x.next

        if x.next is not None: # x不是最后一个结点
            x.next.pre = x.pre

    def show(self):
        '''打印链表'''
        x = self.head
        while x is not None:
            print x.value
            x = x.next

        ################################################
        # 带哨兵的双向循环链表
class DLinkWithSentry(object):
    def __init__(self):
        self.nil = DNode() # 哨兵
        self.nil.next = self.nil # 一个空的链表只由一个哨兵构成，L.nil.next和L.nil.prev同时指向L.nil
        self.nil.prev = self.nil

    def search(self,key):
        x = self.nil.next
        while x != self.nil and x.value != key:
            x = x.next
        return x

    def insert(self, x):
        x.next = self.nil.next
        self.nil.next.prev = x
        self.nil.next = x
        x.prev = self.nil

    def delete(self, x):
        if not isinstance(x,DNode): x = self.search(x)
        if x is None: return
        x.prev.next = x.next
        x.next.prev = x.prev

    def show(self):
        x = self.nil.next
        while x != self.nil:
            print x.value
            x = x.next

################################################
class Node(object):
    def __init__(self,value,next=None):
        self.value = value
        self.next = next

# 单向链表
class Link(object):
    def __init__(self):
        self.head = None
    def search(self,key):
        x = self.head
        while x != None and x.value != key:
            x = x.next
        return x
    def insert(self,x): # 插入到链表头
        if self.head is not None:
            x.next = self.head
        self.head = x
    def delete(self,key):
        prev, x = None, self.head
        #查找第一个值为key的元素x，并保留x前的元素prev
        while x != None and x.value != key:
            prev = x
            x = x.next
        if x is None: return
        if prev: # x不是第一个元素
            prev.next = x.next
        else:
            self.head = x.next
    def show(self):
        x = self.head
        while x != None:
            print x.value
            x = x.next

################################################
# 单链表实现栈 后进先出 FILO
class UnderlowError(Exception):pass # 下溢
class StackL(object):
    def __init__(self):
        self.head = None
    #测试一个栈是否为空
    STACK_EMPTY = lambda self: self.head is None
    #插入元素到栈顶
    def PUSH(self,x):
        if self.head is not None:
            x.next = self.head
        self.head = x
    #将栈顶元素返回并删除
    def POP(self):
        if self.STACK_EMPTY():
            raise UnderlowError("stack is empty")
        x = self.head
        self.head = x.next
        return x
    def show(self):
        x = self.head
        while x is not None:
            print x.value
            x = x.next

################################################
# 队列 先进先出 FIFO
class QueueL(object):
    def __init__(self):
        self.head = self.tail = None
    # 判断队列是否为空
    QUEUE_EMPTY = lambda self: self.head == None
    # 入队
    def ENQUEUE(self, x):
        if self.QUEUE_EMPTY(): #空队列，队头队尾都执行同一个元素
            self.head = self.tail = x
        else: #否则，队头保持不变，新元素放在队尾后
            self.tail.next = x
            self.tail = x
    # 出队
    def DEQUEUE(self):
        if self.QUEUE_EMPTY(): raise UnderlowError("the queue is empty")
        x = self.head
        self.head = x.next
        return x
    def show(self):
        x = self.head
        while x is not None:
            print x.value
            x = x.next

if __name__ == "__main__":
    d = DLink()
    for i in xrange(10):
        d.insert(DNode(i))

    print d.search(5).next.value
    print d.search(5).pre.value
    print d.search(20)
    print '-------------------'
    d.show()