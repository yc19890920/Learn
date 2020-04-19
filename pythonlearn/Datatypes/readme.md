# Python 数据结构与算法 #

Python中常见的数据结构可以统称为容器（container）。
序列（如列表、元组、字符串）、映射（如字典）以及集合（set）是三类主要的容器。




# 常用数据类型 #

## 序列（列表、元组和字符串）
- 序列中的每个元素都有自己的编号。
- Python中有6种内建的序列，其中列表和元组是最常见的类型。
- 其他包括字符串、Unicode字符串、buffer对象和xrange对象。
- 列表是可变的，这是它区别于字符串和元组的最重要的特点，一句话概括即：列表可以修改，而字符串和元组不能。
- 格式化字符串（包含很多其他丰富的转换类型、模板字符串、format等)
- 从列表、元组以及字符串可以“抽象”出序列的一些公共通用方法（不是你想像中的CRUD），这些操作包括：索引（indexing）、分片（sliceing）、加（adding）、乘（multiplying）以及检查某个元素是否属于序列的成员。除此之外，还有计算序列长度、最大最小元素等内置函数。


## 映射（字典）
- 映射中的每个元素都有一个名字，如你所知，这个名字专业的名称叫键。字典（也叫散列表）是Python中唯一内建的映射类型。

## 集合(set、frozenset)




# 高级数据结构 #
在Python中有四种内建的数据结构，分别是List、Tuple、Dictionary以及Set。
大部分的应用程序不需要其他类型的数据结构，但若是真需要也有很多高级数据结构可供选择，例如Collection、Array、Heapq、Bisect、Weakref、Copy以及Pprint。

- Collections
`collections模块包含了内建类型之外的一些有用的工具，例如Counter、defaultdict、OrderedDict、deque以及nametuple。其中Counter、deque以及defaultdict是最常用的类。`
- Array
- Heapq
- Bisect
- Weakref
- Copy
- Pprint
## 文档
- [常用查找数据结构及算法（Python实现）](http://python.jobbole.com/87440/)
- [Python中的高级数据结构](http://blog.jobbole.com/65218/)
- [problem-solving-with-algorithms-and-data-structure-using-python 中文版](https://facert.gitbooks.io/python-data-structure-cn/)
- [Problem Solving with Algorithms and Data Structures](http://interactivepython.org/runestone/static/pythonds/index.html)
- [数据结构](http://www.pythondoc.com/pythontutorial27/datastructures.html)




# 其他高级数据结构 #

# 基础
- Stack栈: 数组实现
- Stack栈: 链表实现
- Queues队列: 数组实现
- Queues队列: 链表实现
- Lists列表: 数组实现 
- Lists列表: 链表实现 

# 索引
- Binary Search Trees 二叉检索树
- AVL Trees (平衡二叉检索树)
- Red-Black Trees 红黑树 
- Open Hash Tables 开放哈希表(Closed Addressing 链地址法)
- Closed Hash Tables  闭合哈希表 (Open Addressing 开放定址法)
- Closed Hash Tables, using buckets 使用桶
- B Trees B树
- B+ Trees B+树

# 排序
- Comparison Sorting 比较式排序
- Bubble Sort 冒泡排序
- Selection Sort 选择排序
- Insertion Sort 插入排序
- Shell Sort 希尔排序
- Merge Sort 归并排序
- Quck Sort 快速排序
- Bucket Sort 桶排序
- Counting Sort 计数排序
- Radix Sort 基数排序

# 堆数据结构
- Heaps 堆
- Binomial Queues 二项队列

# 图 算法
- Breadth-First Search 广度优先搜索
- Depth-First Search 深度优先搜索
- Connected Components 连通性
- Dijkstra’s Shortest Path Dijkstra最短路径
- Prim’s Minimum Cost Spanning Tree 最小生成树
- Topological Sort  拓扑排序
- Floyd-Warshall 算法(解决任意两点间的最短路径的一种算法) 
- 基于Kruskal算法的最小生成树的构建

# 动态编程
- 计算 Fibonacci 数

# 参考资料
- [可视化的数据结构和算法](http://coolshell.cn/articles/4671.html)
- [Problem Solving with Algorithms and Data Structures](http://interactivepython.org/courselib/static/pythonds/index.html)
- [有哪些用 Python 语言讲算法和数据结构的书？](https://www.zhihu.com/question/19889750)