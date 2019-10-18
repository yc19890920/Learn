lru_cache

1 . cache的value是能是不可变对象。
2. 在并发时，多个线程对缓存进行读写，那么必须对set()操作加锁。TODO 实现一个支持并发访问的LRU cache
3. value不能设置过期时间，而常用的redis和memcached都支持给value设置expire time。TODO 实现一个支持expire的LRU cache
