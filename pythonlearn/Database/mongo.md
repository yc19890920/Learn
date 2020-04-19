
```
>>> import pymongo
>>> conn = pymongo.Connection("localhost", 27017)

MongoDB URI:
mongo_cfg = {
    'host': settings.MONGO_HOST,
    'port': settings.MONGO_PORT,
    'username': settings.MONGO_USER,
    'dbname': settings.MONGO_DBNAME,
    'password': settings.MONGO_PWD,
}
mongo = pymongo.MongoClient(
        host='mongodb://{username}:{password}@{host}:{port}/{dbname}'.format(**mongo_cfg))
```

## 文档
- [Python 操作 MongoDB](http://www.cnblogs.com/hhh5460/p/5838516.html)
- [MongoDB 更新文档 update](http://makaidong.com/softn/1/1003_10529495.html)
- [mongodb中使用正则表达式范例(pymongo演示)](http://www.sharejs.com/codes/python/9009)
- [pymongo多结果进行多列排序](http://www.sharejs.com/codes/python/6687)
- [初窥Python（一）——使用pymongo连接MongoDB](http://xitongjiagoushi.blog.51cto.com/9975742/1657096)
- [Pymongo 3.03中文文档(翻译)](https://juejin.im/entry/59a512b1f265da2499603c4b)
- [MongoDB 教程](http://www.runoob.com/mongodb/mongodb-tutorial.html)
- [MongoDB学习 (六)：查询](http://www.cnblogs.com/egger/archive/2013/06/14/3135847.html)
- [MongoDB的条件查询](http://www.cnblogs.com/navy235/archive/2012/05/03/2480758.html)
- [浅述MongoDB的管理操作](http://www.cnblogs.com/navy235/archive/2012/05/04/2482397.html)
- [Mongoose 模型提供了 find, findOne, 和 findById 方法用于文档查询。](http://www.cnblogs.com/navy235/archive/2012/05/03/2480770.html)
- [MongoDB 分页查询的方法及性能](http://www.cnblogs.com/wuxl360/p/5432284.html)
- [MongoDB 分页查询的方法及性能](http://blog.jobbole.com/80464/)
- [MongoDB 3.0 用户创建](http://www.cnblogs.com/zhoujinyi/p/4610050.html)
- [Mongodb使用](http://www.cnblogs.com/DjangoBlog/p/3966202.html)
- [mongodb常用命令](http://www.cnblogs.com/cxd4321/archive/2011/06/24/2089051.html)
- [学习MongoDB 七： MongoDB索引（索引基本操作）（一）](http://lib.csdn.net/article/64/46658?knId=1777)