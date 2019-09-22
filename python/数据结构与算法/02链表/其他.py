# -*- coding: utf-8 -*-
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