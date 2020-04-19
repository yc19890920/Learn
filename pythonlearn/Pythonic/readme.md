
> **1. 链式比较**

```
if 1 < a < 7: pass
```


> **2. 交换变量**

```
x, y = 1, 2
x, y = y, x
print x, y
# 2 1
```


> **3. 三目运算符**

```
x, y = 1, 2
z = x if x > y else y
print z
# 2
z = x > y and x or y
print z
# 2
```


> **4. 拼接字符列表时，用join方法去实现**

```
a=['1', '2']
b = ','.join(a)
print b
# 1,2
```

> **5. 字符串反转**

```
s = '123   abc'
T = s[::-1]
# cba   321
```


> **6. 使用列表或者字典comprehension**

```
mylist = range(20)
T = filter(lambda x: x%2==0, mylist)
print T
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
T = [i for i in mylist if i%2]
print T
# [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
################
d = [{'name': 'lucy', 'email': 'lucy@g.com'}, {'name': 'lily', 'email': 'lily@g.com'}]
{ d['name']: d['email'] for d in user_list if 'email' in d }
```


> **7. 真值测试。条件判断时，避免直接和True, False, None进行比较(==)** 

```
a = True #( Flase, None, '', 0, [], {}, (), set(), )
if a: pass
if not a: pass
```


> **8. 使用enumerate代替for循环中的index变量访问**

```
myL = [1, 2, 3]
for index, ele in enumerate(myL):
    print  index, ele
```


> **9. 避免使用可变(mutable)变量作为函数参数的默认初始化值**

```
# bad
def function(l = []):
    l.append(1)
    return l
    
print function()
print function()
print function()
# [1]
# [1, 1]
# [1, 1, 1]

######################
# good 使用None作为可变对象占位符
def function(l=None):
    l = l or []
    l.append(1)
    return l
    
print function([1])
print function([2])
print function()
print function()
# [1, 1]
# [2, 1]
# [1]
# [1]
```

> **10. 用dict对象完成switch...case...的功能**

```
import operator as op
OPEEATOR_MAPPER = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv}
def apply_operation(operator, left_operand, right_operand):
    return OPEEATOR_MAPPER[operator](left_operand, right_operand)

print apply_operation('+', 1, 2)
# 3
```

> **11. 访问tuple的数据项时，可以用namedtuple代替index的方式访问**

```
# bad
rows = (('lily', 20, 2000), ('lucy', 19, 2500))
for row in rows:
    print '{}`age is {}, salary is {} '.format(row[0], row[1], row[2])

# good
from collections import  namedtuple
Employee = namedtuple('Employee', 'name, age, salary')
for row in rows:
    employee = Employee._make(row)
    print '{}`age is {}, salary is {} '.format(employee.name, employee.age, employee.salary)
```


> **12. 字典的默认值**

```
dic = {'name':'Tim', 'age':23}  
 
dic['workage'] = dic.get('workage',0) + 1
#dic = {'age': 23, 'workage': 1, 'name': 'Tim'}

# 嵌套字典
from collections import defaultdict

_nested_dict = lambda: defaultdict(_nested_dict)
nestedD = _nested_dict()

data = [
    # user_id, task_name, domain, success, err_1, err_2, err_3
    (2369, '201708091111-2369-20', 'qq.com', 100, 1, 2, 15),
    (2369, '201708091111-2369-20', 'qq.com', 500, 1, 0, 15),
    (2369, '201708091111-2369-20', '163.com', 120, 1, 2, 17),
    (2369, '201708101111-2369-20', '163.com', 150, 1, 2, 17),
    (3469, '201708091113-3469-28', 'qq.com', 300, 10, 50, 100),
    (2555, '201708091113-2555-28', '*', 180, 10, 10, 0),
]

for res in data:
    user_id, task_name, domain, success, err_1, err_2, err_3 = res
    _D = nestedD[user_id][task_name][domain]
    _D['success'] = _D.get('success', 0) + success
    _D['err_1'] = _D.get('err_1', 0) + err_1
    _D['err_2'] = _D.get('err_2', 0) + err_2
    _D['err_3'] = _D.get('err_3', 0) + err_3

print nestedD[2369]['201708091111-2369-20']['163.com']['success']

pprint.pprint(
    nestedD
)

#################################################
# 默认字典的简单树状表达
import json
import collections
tree = lambda: collections.defaultdict(tree)
root = tree()
root['menu']['id'] = 'file'
root['menu']['value'] = 'File'
root['menu']['menuitems']['new']['value'] = 'New'
root['menu']['menuitems']['new']['onclick'] = 'new();'
root['menu']['menuitems']['open']['value'] = 'Open'
root['menu']['menuitems']['open']['onclick'] = 'open();'
root['menu']['menuitems']['close']['value'] = 'Close'
root['menu']['menuitems']['close']['onclick'] = 'close();'
print json.dumps(root, sort_keys=True, indent=4, separators=(',', ': '))
{
    "menu": {
        "id": "file",
        "menuitems": {
            "close": {
                "onclick": "close();",
                "value": "Close"
            },
            "new": {
                "onclick": "new();",
                "value": "New"
            },
            "open": {
                "onclick": "open();",
                "value": "Open"
            }
        },
        "value": "File"
    }
}
```

> **13. for…else…语句**
> 即在for 循环中，如果没有从任何一个break中退出，则会执行和for对应的else，只要从break中退出了，则else部分不执行。

```
for x in xrange(10):
    if x==100:
        break
    if x==3:
        break
else:
    print 'process...'
```

> **14. zip创建键值对**
> zip方法返回的是一个元组，用它来创建键值对，简单明了。

```
keys = ['Name', 'Sex', 'Age']
values = ['Tim', 'Male', 23]

dic = dict(zip(keys, values))
# {'Age': 23, 'Name': 'Tim', 'Sex': 'Male'}
```

> **15. 列表以及迭代器的压缩和解压缩**

```
a = [1, 2, 3]
b = ['a', 'b', 'c']
z = zip(a, b)
print z
# [(1, 'a'), (2, 'b'), (3, 'c')]
T = zip(*z)
print T
# [(1, 2, 3), ('a', 'b', 'c')]
```


> **16. 列表相邻元素压缩器**

```
>>> a = [1, 2, 3, 4, 5, 6]
>>> zip(*([iter(a)] * 2))
[(1, 2), (3, 4), (5, 6)]

>>> group_adjacent = lambda a, k: zip(*([iter(a)] * k))
>>> group_adjacent(a, 3)
[(1, 2, 3), (4, 5, 6)]
>>> group_adjacent(a, 2)
[(1, 2), (3, 4), (5, 6)]
>>> group_adjacent(a, 1)
[(1,), (2,), (3,), (4,), (5,), (6,)]
```

> **17. 列表展开 **

```
a = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
flatten = lambda L: [y for x in L for y in flatten(x)] if isinstance(L, list) else [L]
print flatten(a)
# [1, 2, 3, 4, 5, 6, 7, 8]
```


> **18. 格式化字符时多使用format函数, 除非数据库操作**


> **19. 一切皆对象**
>>`可以函数作为参数，类似技巧可以用来简化代码`


> **20. 防御式编程EAFP vs LBYL**


> **21. 用isinstance来判断对象的类型**


> **22. 用with管理操作资源的上下文环境**


> **23. 使用generator返回耗费内存的对象**


## 文档
- [Hidden features of Python](https://stackoverflow.com/questions/101268/hidden-features-of-python)