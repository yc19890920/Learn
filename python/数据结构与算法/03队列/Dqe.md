# list

# queue

# deque
#### 在多线程下，deque双端队列是安全的，可以放心使用。 
- append       ppend默认从集合的右边增加数组元素，
- appendleft   另一个appendleft可以从集合的左边增加元素
- extend       deque是通过extend方法初始化集合元素的，同时你可以通过extendleft将结合元素从“左边”加入到集合中
- extendleft
- pop          pop和popleft方法分别用于从集合中取出元素
- popleft
- rotate      是队列的旋转操作，Right rotate(正参数)是将右端的元素移动到左端，而Left rotate(负参数)则相反。

- [容器(Collections)](https://eastlakeside.gitbooks.io/interpy-zh/content/collections/collections.html)


```
>>> import collections
>>> d = collections.deque(xrange(10))
>>> d
deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> d.rotate(2)  #  将右端的两个元素移动到左端
>>> d
deque([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])
>>> d = collections.deque(xrange(10))
>>> d.rotate(-2) #  将左端的两个元素移动到右端
>>> d
deque([2, 3, 4, 5, 6, 7, 8, 9, 0, 1])
>>> 
```


1. 把链表当作堆栈使用
- 链表方法使得链表可以很方便的做为一个堆栈来使用，堆栈作为特定的数据结构，最先进入的元素最后一个被释放(后进先出)。
- 用 append() 方法可以把一个元素添加到堆栈顶。用不指定索引的 pop() 方法可以把一个元素从堆栈顶释放出来。
```
>>> stack = [3, 4, 5]
>>> stack.append(6)
>>> stack.append(7)
>>> stack
[3, 4, 5, 6, 7]
>>> stack.pop()
7
>>> stack
[3, 4, 5, 6]
>>> stack.pop()
6
>>> stack.pop()
5
>>> stack
[3, 4]
```

2. 把链表当作队列使用
- 把链表当做队列使用，队列作为特定的数据结构，最先进入的元素最先释放(先进先出)。 
- 不过，列表这样用效率不高。 相对来说从列表末尾添加和弹出很快；在头部插入和弹出很慢(因为为了一个元素，要移动整个列表中的所有元素)。
要实现队列，使用 collections.deque，它为在首尾两端快速插入和删除而设计。
```
>>> from collections import deque
>>> queue = deque(["Eric", "John", "Michael"])
>>> queue.append("Terry")           # Terry arrives
>>> queue.append("Graham")          # Graham arrives
>>> queue.popleft()                 # The first to arrive now leaves
'Eric'
>>> queue.popleft()                 # The second to arrive now leaves
'John'
>>> queue                           # Remaining queue in order of arrival
deque(['Michael', 'Terry', 'Graham'])
```

