在数据库中有两种通用的方法确保在并发更新时修改不丢失：

## 悲观并发控制（Pessimistic concurrency control）
这在关系型数据库中被广泛的使用，假设冲突的更改经常发生，为了解决冲突我们把访问区块化。
典型的例子是在读一行数据前锁定这行，然后确保只有加锁的那个线程可以修改这行数据。


## 乐观并发控制（Optimistic concurrency control）：
被Elasticsearch使用，假设冲突不经常发生，也不区块化访问，然而，如果在读写过程中数据发生了变化，更新操作将失败。
这时候由程序决定在失败后如何解决冲突。实际情况中，可以重新尝试更新，刷新数据（重新读取）或者直接反馈给用户。



- [Elasticsearch 处理冲突（并发控制）](https://es.xiaoleilu.com/030_Data/40_Version_control.html)