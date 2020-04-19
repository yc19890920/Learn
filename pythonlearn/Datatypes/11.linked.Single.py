# -*- coding: utf-8 -*-

class Node(object):
    '''该类实例化一个元素节点.'''

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class LinkedList(object):
    '''实现一个单向链表.'''

    def __init__(self):
        ''' 初始化链表: 初始化时,为一个空链表.链表有两个标示head和tail都赋值None.'''
        self.head = None
        self.tail = None

    def append(self, data):
        '''
        向链表新增元素:
        1. 如果该链表是一个空链表,则链表head和tail都指向传进来的node节点.
        2. 如果链表非空,则self.tail.next = node.next 指向新插入元素.
        3. tail指向新插入的元素节点.
        '''
        node = Node(data)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def insert(self, index, value):
        '''向链表插入一个元素node.
        1. 从链表头开始遍历链表,当查找的index小于要插入索引的位置时，依次
           指向下一个元素节点.直到找到要插入节点的索引位置.
        2. 首先将插入的值,通过Node类实例化一个元素node.然后将它的next指针
           指向它的下一个元素.即当前新元素节点之前的元素索引位置.
        3. 将当前元素索引指向新插入元素node.
        '''
        cur = self.head
        cur_index = 0
        while cur_index < index - 1:
            cur = cur.next
            if cur.next is None:
                raise Exception('list length less than index')
            cur_index += 1
        node = Node(value)
        node.next = cur.next
        cur.next = node
        if cur.next is None:
            self.tail = node

    def remove(self, index):
        '''从链表中删除一个元素节点.
        1. 首先找到要删除的元素节点索引.
        2. 然后将当前节点的next指向下一个下一个元素节点.
        '''
        cur = self.head
        cur_index = 0
        while cur_index < index-1:
            cur = cur.next
            if cur is None:
                raise Exception('list length less than index')
            cur_index +=1
        cur.next = cur.next.next
        if cur.next is None:
            self.tail = cur

    def iter(self):
        '''
        返回一个链表迭代器.
        1. 首先判断该链表是否为一个空链表。如果时一个空链表,直接返回.
        2. 如果是一个非空链表,首先指针指向head节点,然后将head节点data
           返回.然后while循环,条件是下一个指针元素为真.然后弹出下一个元
           素data,直到遍历到最后一个元素.
        '''
        if not self.head:
            return
        cur = self.head
        yield cur.value
        while cur.next:
            cur = cur.next
            yield cur.value

if __name__ == "__main__":
    linked_list = LinkedList()

    # 循环插入元素
    for i in range(10):
        linked_list.append(i)

    # 向元素插入一个元素
    linked_list.insert(0, 40)

    # 向元素删除一个元素
    linked_list.remove(4)

    # 遍历该链表
    for node in linked_list.iter():
        print node