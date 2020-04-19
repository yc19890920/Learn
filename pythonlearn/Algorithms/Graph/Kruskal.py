#coding:utf-8

# 以全局变量X定义节点集合，即类似{'A':'A','B':'B','C':'C','D':'D'},如果A、B两点联通，则会更改为{'A':'B','B':'B",...},即任何两点联通之后，两点的值value将相同。
X = dict()

# 各点的初始等级均为0,如果被做为连接的的末端，则增加1
R = dict()

#设置X R的初始值
# makeset函数，用于初始化 vertices
def make_set(point):
    X[point] = point
    R[point] = 0

# 节点的联通分量
# find函数，用于找到根节点
def find(point):
    if X[point] != point:
        X[point] = find(X[point])
    return X[point]

#连接两个分量（节点）
# union 函数，用于联通两个子块
def union(point1, point2):
    r1 = find(point1)
    r2 = find(point2)
    if r1 != r2:
        if R[r1] > R[r2]:
            X[r2] = r1
        else:
            X[r1] = r2
            if R[r1] == R[r2]: R[r2] += 1

import heapq
#KRUSKAL算法实现
def kruskal(graph):
    for vertice in graph['vertices']:
        make_set(vertice)

    minu_tree = set()

    edges = list(graph['edges'])

    heapq.heapify(edges)
    edges.sort()                    #按照边长从小到达排序
    for edge in edges:
        weight, vertice1, vertice2 = edge
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            minu_tree.add(edge)
    return minu_tree



if __name__=="__main__":
    graph = {
        'vertices': ['A', 'B', 'C', 'D', 'E', 'F', 'G', "H", "I"],
        'edges': set([
            (7, "A", "B"), (5, "A", "D"),
            (8, "B", "C"), (9, "B", "D"),
            (7, "B", "E"), (5, "C", "E"),
            (15, "D", "E"), (6, "D", "F"),
            (8, "E", "F"), (9, "E", "G"),
            (11, "F", "G"), (9, "H", "I"),
        ])

    }

    result = kruskal(graph)
    print result
    # set([(7, 'B', 'E'), (5, 'A', 'D'), (9, 'E', 'G'), (6, 'D', 'F'), (5, 'C', 'E'), (9, 'H', 'I'), (7, 'A', 'B')])
