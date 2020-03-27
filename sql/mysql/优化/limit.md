## 当只要一行数据时使用 LIMIT 1
当你查询表的有些时候，你已经知道结果只会有一条结果，但因为你可能需要去fetch游标，或是你也许会去检查返回的记录数。
在这种情况下，加上 LIMIT 1 可以增加性能。这样一样，MySQL数据库引擎会在找到一条数据后停止搜索，而不是继续往后查少下一条符合记录的数据。
下面的示例，只是为了找一下是否有“中国”的用户，很明显，后面的会比前面的更有效率。(请注意，第一条中是Select *，第二条是Select 1) 

- [MySQL order by 与 limit 的优化](https://my.oschina.net/leejun2005/blog/124565)
- [MySQL 中随机抽样：order by rand limit 的替代方案](https://my.oschina.net/leejun2005/blog/99167)
- [MySQL Limit 性能优化及分页数据性能优化](https://my.oschina.net/No5stranger/blog/158202)
- [mysql limit 性能优化](https://www.jianshu.com/p/efecd0b66c55)
- [MYSQL分页limit速度太慢优化方法](http://ourmysql.com/archives/1451)

分页数据性能优化：

1、对于数据量较大数据表，可以建立主键和索引字段建立索引表，通过索引表查询相应的主键，在通过主键查询数据量的数据表；

2、如果对于有where 条件，又想走索引用limit的，必须设计一个索引，将where 放第一位，limit用到的主键放第2位，而且只能select 主键！这样能提高读取速度

3、利用in：先通过where条件取得相应的主键值，然后利用主键值查询相应的字段值。
