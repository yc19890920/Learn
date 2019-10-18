
- [分布式锁的几种实现方式](https://juejin.im/entry/596c51015188252a6758998f)
- [如何用 redis 造一把分布式锁](https://wecatch.me/blog/2016/08/20/distributed-lock-with-redis/)
- [使用 Redis 实现分布式锁](https://strawhatfy.github.io/2015/07/09/Distributed%20locks%20with%20Redis/)
- [python中，用Redis构建分布式锁](https://www.jianshu.com/p/261c84ce9a6c)

## 1. 使用Redis实现分布式锁
```
* WATCH, MULTI, EXEC, DISCARD事务机制实现分布式锁
Redis支持基本的事务操作
MULTI
some redis command
EXEC

以上被MULTI和EXEC包裹的redis命令，保证所有事务内的命令将会串行顺序执行，
保证不会在事务的执行过程中被其他客户端打断。
而WATCH命令能够监视某个键，当事务执行时，如果被监视的键被其他客户端修改了值，事务运行失败，
返回相应错误（被事务运行客户端在事务内修改了值，不会造成事务运行失败）。 

运用Redis事务所支持的以上特性，可以实现一个分布式锁功能。Python代码如下：
# -*- coding: utf-8 -*-
def acqure_lock_with_watch(conn, lockname, acquire_timeout=10):
    pipe = conn.pipeline()
    end = time.time() + acquire_timeout
    lockname = 'lock:' + lockname

    while time.time() < end:
        try:
            pipe.watch(lockname)
            pipe.multi()  # 开启事务
            # 事务具体内容，对lockname的值进行更新
            pipe.execute()
            return True
        except redis.exceptions.WatchError:
            # 事务运行期间，有其他客户端改变了lockname的值，抛出异常，进行重试操作
            pass

    return False
    
通过WATCH命令监视某个键，当该键未被其他客户端修改值时，事务成功执行。当事务运行过程中，发现该值被其他客户端更新了值，任务失败，进行重试。


* SETNX实现分布式锁
SETNX：当指定键不存在时，向Redis中添加一个键值对。Redis客户端保证对统一键名称，多个客户端同时设置其值时，只有一个客户端能够设置成功的原子性。
# -*- coding: utf-8 -*-
def acquire_lock_with_timeout(
        conn, lockname, acquire_timeout=10, lock_timeout=10):
    identifire = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    lock_timeout = int(math.ceil(lock_timeout))

    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.setnx(lockname, identifire):  # 以锁名称为键，uuid的值为值，redis服务器setnx保证了只能有一个客户端成功设置键的原子性
            conn.expire(lockname, lock_timeout)  # 设置键的过期时间，过期自动剔除，释放锁
            return identifire
        elif not conn.ttl(lockname):  # 当锁未被设置过期时间时，重新设置其过期时间
            conn.expire(lockname, lock_timeout)

        time.sleep(0.001)

    return False
    
以上，利用SETNX的原子特性，和Redis的键过期特性，实现了自动过期释放的分布式锁。
```

## 基于 Redis 做分布式锁
基于 redis 的 setnx()、expire() 方法做分布式锁
setnx()
setnx 的含义就是 SET if Not Exists，其主要有两个参数 setnx(key, value)。
该方法是原子的，如果 key 不存在，则设置当前 key 成功，返回 1；如果当前 key 已经存在，则设置当前 key 失败，返回 0。

expire()
expire 设置过期时间，要注意的是 setnx 命令不能设置 key 的超时时间，只能通过 expire() 来对 key 设置。

使用步骤
1、setnx(lockkey, 1) 如果返回 0，则说明占位失败；如果返回 1，则说明占位成功
2、expire() 命令对 lockkey 设置超时时间，为的是避免死锁问题。
3、执行完业务代码后，可以通过 delete 命令删除 key。

这个方案其实是可以解决日常工作中的需求的，但从技术方案的探讨上来说，可能还有一些可以完善的地方。
比如，如果在第一步 setnx 执行成功后，在 expire() 命令执行成功前，发生了宕机的现象，那么就依然会出现死锁的问题，所以如果要对其进行完善的话，可以使用 redis 的 setnx()、get() 和 getset() 方法来实现分布式锁。


## 基于 redis 的 setnx()、get()、getset()方法做分布式锁
这个方案的背景主要是在 setnx() 和 expire() 的方案上针对可能存在的死锁问题，做了一些优化。
getset()
这个命令主要有两个参数 getset(key，newValue)。
该方法是原子的，对 key 设置 newValue 这个值，并且返回 key 原来的旧值。
假设 key 原来是不存在的，那么多次执行这个命令，会出现下边的效果：

    getset(key, “value1”) 返回 null 此时 key 的值会被设置为 value1
    getset(key, “value2”) 返回 value1 此时 key 的值会被设置为 value2
    依次类推！

使用步骤

    setnx(lockkey, 当前时间+过期超时时间)，如果返回 1，则获取锁成功；如果返回 0 则没有获取到锁，转向 2。
    get(lockkey) 获取值 oldExpireTime ，并将这个 value 值与当前的系统时间进行比较，如果小于当前系统时间，则认为这个锁已经超时，可以允许别的请求重新获取，转向 3。
    计算 newExpireTime = 当前时间+过期超时时间，然后 getset(lockkey, newExpireTime) 会返回当前 lockkey 的值currentExpireTime。
    判断 currentExpireTime 与 oldExpireTime 是否相等，如果相等，说明当前 getset 设置成功，获取到了锁。如果不相等，说明这个锁又被别的请求获取走了，那么当前请求可以直接返回失败，或者继续重试。
    在获取到锁之后，当前线程可以开始自己的业务处理，当处理完毕后，比较自己的处理时间和对于锁设置的超时时间，如果小于锁设置的超时时间，则直接执行 delete 释放锁；如果大于锁设置的超时时间，则不需要再锁进行处理。


