
## 任务队列

### 一般队列
```
生产者 LPUSH
消费者 RPOP

BRPOP 和RPOP类似，但是当列表中没有元素时，BRPOP会一直阻塞住链接，直到有新元素加入
```


### 优先队列
```
BLPOP key [key ...] timeout,同时检测多个键，如果所有键都没有元素则阻塞，如果其中有一个键有元素，则从该键中弹出元素
如果都有，则从左到右的顺序取第一个键中的一个元素

BLPOP queue:1 queue:2 queue:3 0
```

### 2.简单优先级的队列

假设一种简单的需求，只需要高优先级的比低优先级的任务率先处理掉。其他任务之间的顺序一概不管，这种我们只需要在在遇到高优先级任务的时候将它塞到队列的前头，而不是push到最后面即可。
因为我们的队列是使用的redis的 list,所以很容易实现。

遇到高优先级的使用rpush 遇到低优先级的使用lpush。

```
redis> lpush tasklist 'im task 01'
redis> lpush tasklist 'im task 02'
redis> rpush tasklist 'im high task 01'
redis> rpush tasklist 'im high task 01'
redis> lpush tasklist 'im task 03'
redis> rpush tasklist 'im high task 03'
```
随后会看到，高优先级的总是比低优先级的率先执行。但是这个方案的缺点是高优先级的任务之间的执行顺序是先进后出的。


### 3.较为完善的队列

例子2中只是简单的将高优先级的任务塞到队列最前面，低优先级的塞到最后面。这样保证不了高优先级任务之间的顺序。
假设当所有的任务都是高优先级的话，那么他们的执行顺序将是相反的。这样明显违背了队列的FIFO原则。
不过只要稍加改进就可以完善我们的队列。
跟使用rabbitmq一样，我们设置两个队列，一个高优先级一个低优先级的队列。高优先级任务放到高队列中，低的放在低优先队列中。redis和rabbitmq不同的是它可以要求队列消费者从哪个队列里面先读。
```
def main():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    while 1:
        result = r.brpop(['high_task_queue', 'low_task_queue'], 0)
        handle(result[1])
```
上面的代码，会阻塞地从'high_task_queue', 'low_task_queue'这两个队列里面取数据，如果第一个没有再从第二个里面取。
所以只需要将队列消费者做这样的改进便可以达到目的。

```
redis> lpush low_task_queue low001
redis> lpush low_task_queue low002
redis> lpush low_task_queue low003
redis> lpush low_task_queue low004
redis> lpush high_task_queue low001
redis> lpush high_task_queue low002
redis> lpush high_task_queue low003
redis> lpush high_task_queue low004
```

通过上面的测试看到，高优先级的会被率先执行，并且高优先级之间也是保证了FIFO的原则。
这种方案我们可以支持不同阶段的优先级队列，例如高中低三个级别或者更多的级别都可以。

