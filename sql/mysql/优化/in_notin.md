## mysql not in 如何进行性能优化 

优化原则：小表驱动大表，即小的数据集驱动大的数据集。

```
select * from A where id in (select id from B)
等价于:
for select id from B
for select * from A where A.id = B.id
```

当B表的数据集必须小于A表的数据集时，用in优于exists。
```
select * from A where exists (select 1 from B where B.id = A.id)
等价于
for select * from A
for select * from B where B.id = A.id
```
注意：A表与B表的ID字段应建立索引。


### mysql exists与in 具体不同在什地方
```
in 是把外表和内表作hash 连接；
exists 是对外表作loop循环，每次loop循环再对内表进行查询。

一直以来认为exists比in效率高的说法是不准确的。
如果查询的两个表大小相当，那么用in和exists差别不大。
如果两个表中一个较小，一个是大表，则子查询表大的用exists，子查询表小的用in。
```


## MYSQL NOT IN优化
Mysql 下 SQL 优化NOT IN （除了把NOT IN转化为LEFT JOIN外，可优化影响的数据行数）  
除了把NOT IN转化为LEFT JOIN外，可通过优化业务逻辑，减少了查询涉及到的返回的数据，从而达到优化查询的目的。

NOT IN的（除了转化为LEFT JOIN外，可以通过业务逻辑）优化：
 缩小了博文的数据范围，定义在10天内发表的博文，取出200条，然后排除重复，按照发表时间顺序显示。
如果不加 博文的时间范围限制，返回满足条件的全部的博文数据列表多达27万条记录，mysql会分配很大内存来存放数据。
加上博文的时间范围，则返回满足条件的全部的博文数据列减少了很多。
再次explain 此sql语句，会发现wp_posts表涉及到的行为248行。 执行sql语句 发现速度提升不少。


## 实例
1. select * from A where id in (select id from B), in优化改为 INNER JOIN
改为： SELECT A.* FROM A INNER JOIN B ON A.id = B.id

2. select * from A where id not in (select id from B), not in优化改为 LEFT JOIN
改为： SELECT A.* FROM A LEFT JOIN B ON A.id = B.id WHERE B.id is NULL;


## PS：那我们死活都不能用 IN 和 NOT IN 了么？并没有，一位大神曾经说过，如果是确定且有限的集合时，可以使用。如 IN （0，1，2）。


