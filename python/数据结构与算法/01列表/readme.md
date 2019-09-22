线性结构

## 时间复杂度
 操作                                  | 平均时间复杂度 |
--------------------------------------|----------------|
list[index]                           | O(1)           |
list.append                           | O(1)           |
list.insert                           | O(n)           |
list.pop(index), default last element | O(1)           |
list.remove                           | O(n)           |

## Python列表函数 #
| 序号 | 方法 | 描述 |
| --- | --- | --- |
| 1 | list.append(obj) | 在列表末尾添加新的对象 | 
| 2 | list.count(obj)  | 统计某个元素在列表中出现的次数 |
| 3	| list.extend(seq) | 在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）| 
| 4	| list.index(obj)  | 从列表中找出某个值第一个匹配项的索引位置 | 
| 5	| list.insert(index, obj) | 将对象插入列表| 
| 6	| list.pop(obj=list[-1]) | 移除列表中的一个元素（默认最后一个元素），并且返回该元素的值 | 
| 7	| list.remove(obj) | 移除列表中某个值的第一个匹配项（remove 方法用于移除列表中的某个匹配元素，如果有多个匹配，则移除第一个。） | 
| 8	| list.reverse() | 反向列表中元素 | 
| 9	| list.sort([func]) | 对原列表进行排序 | 