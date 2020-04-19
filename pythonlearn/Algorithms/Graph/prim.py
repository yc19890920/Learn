# -*- coding: utf-8

'''
prim算法是实现最简单的最小生成树（MST）算法，适合于稠密图。
要实现Prim算法，我们主要关注的是增量的变化，也就是从每个非树顶点到树顶点的最短距离，使得最后生成一棵包括所有顶点的树，并且这棵树的边权值之和最小。


'''

from collections import defaultdict
from heapq import heapify, heappop, heappush

def prim( nodes, edges ):
    conn = defaultdict( list )
    for n1,n2,c in edges:
        conn[ n1 ].append( (c, n1, n2) )
        conn[ n2 ].append( (c, n2, n1) )
    """
    经过上述操作，将edges列表中各项归类成以某点为dictionary的key，其value则是其相邻的点以及边长。如下：

    defaultdict(<type 'list'>, {'A': [(7, 'A', 'B'), (5, 'A', 'D')],
                                'C': [(8, 'C', 'B'), (5, 'C', 'E')],
                                'B': [(7, 'B', 'A'), (8, 'B', 'C'), (9, 'B', 'D'), (7, 'B', 'E')],
                                'E': [(7, 'E', 'B'), (5, 'E', 'C'), (15, 'E', 'D'), (8, 'E', 'F'), (9, 'E', 'G')],
                                'D': [(5, 'D', 'A'), (9, 'D', 'B'), (15, 'D', 'E'), (6, 'D', 'F')],
                                'G': [(9, 'G', 'E'), (11, 'G', 'F')],
                                'F': [(6, 'F', 'D'), (8, 'F', 'E'), (11, 'F', 'G')]})

    """
    mst = [] #存储最小生成树结果
    used = set( nodes[ 0 ] )
    """
    nodes是顶点列表，nodes = list("ABCDEFG")===>nodes=['A', 'B', 'C', 'D', 'E', 'F', 'G']
    >> used=set(nodes[0])
    >> used
    set(['A'])
    也就是，首先选一个点（这个点是可以任意选的），以这个点为起点，找其相邻点，以及最短边长。
    """
    #得到 usable_edges 中顶点是'A'（nodes[0]='A')的相邻点list，即 conn['A']=[(7,'A','B'),(5,'A','D')]
    usable_edges = conn[ nodes[0] ][:]
    # 将 usable_edges 加入到堆中，并能够实现用heappop从其中动态取出最小值。
    heapify( usable_edges )

    while usable_edges:
        # 得到某个定点（做为 usable_edges 的键）与相邻点距离（相邻点和边长/距离做为该键的值）最小值，并同时从堆中清除。
        cost, n1, n2 = heappop( usable_edges )
        if n2 not in used:
            # 在used中有第一选定的点'A'，上面得到了距离A点最近的点'D',举例是5。将'd'追加到used中
            used.add( n2 )
            # 将 n1, n2, cost，第一次循环就是('A','D',5) append into mst
            mst.append( ( n1, n2, cost ) )

            # 再找与 'D' 相邻的点，如果没有在heap中，则应用heappush压入堆内，以加入排序行列
            for e in conn[ n2 ]:
                if e[ 2 ] not in used:
                    heappush( usable_edges, e )
    return mst

if __name__ == "__main__":
    nodes = list("ABCDEFGHI")
    edges = [
        ("A", "B", 7), ("A", "D", 5),
        ("B", "C", 8), ("B", "D", 9),
        ("B", "E", 7), ("C", "E", 5),
        ("D", "E", 15), ("D", "F", 6),
        ("E", "F", 8), ("E", "G", 9),
        ("F", "G", 11), ("H", "I", 9)
    ]
    res = prim( nodes, edges )
    print res
    # [('A', 'D', 5), ('D', 'F', 6), ('A', 'B', 7), ('B', 'E', 7), ('E', 'C', 5), ('E', 'G', 9)]


