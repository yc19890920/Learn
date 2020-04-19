
# Python 多线程

- 线程是一个分离无顺序依赖关系任务的技术。
- 在某些任务运行于后台的时候应用程序会变得迟缓，线程可以提升其速度。一个有关的用途是在 I/O 的同时其它线程可以并行计算。

> 多线程应用程序的主要挑战是协调线程，诸如线程间共享数据或其它资源。
> 为了达到那个目的，线程模块提供了许多同步化的原生支持，包括： **锁，事件，条件变量和信号灯。**
```
尽管这些工具很强大，微小的设计错误也可能造成难以挽回的故障。
因此，任务协调的首选方法是把对一个资源的所有访问集中在一个单独的线程中，然后使用 Queue 模块用那个线程服务其他线程的请求。
为内部线程通信和协调而使用 Queue.Queue 对象的应用程序更易于设计，更可读，并且更可靠。
```

## 文档
- [Python—进程、线程、协程](http://www.cnblogs.com/melonjiang/p/5307705.html)
- [ThreadLocal](https://www.ctolib.com/docs/sfile/explore-python/Process-Thread-Coroutine/threadlocal.html)
- [Python线程指南](http://www.cnblogs.com/huxi/archive/2010/06/26/1765808.html)
- [Python模块学习：threading 多线程控制和处理](http://python.jobbole.com/81546/)
- [Python：使用threading模块实现多线程（转）](http://www.cszhi.com/20130528/python-threading.html)
- [17.1. threading - 基于线程的并行性](http://python.usyiyi.cn/documents/python_352/library/threading.html)
- [Python 多线程和多进程编程总结](https://tracholar.github.io/wiki/python/python-multiprocessing-tutorial.html)
- [扯扯python的多线程的同步锁 Lock RLock Semaphore Event Condition](http://xiaorui.cc/2015/07/10/%E6%89%AF%E6%89%AFpython%E7%9A%84%E5%A4%9A%E7%BA%BF%E7%A8%8B%E7%9A%84%E5%90%8C%E6%AD%A5%E9%94%81-lock-rlock-semaphore-event-condition/)


# Python 多线程
> 线程在执行过程中与进程还是有区别的。每个独立的线程有一个程序运行的入口、顺序执行序列和程序的出口。但是线程不能够独立执行，必须依存在应用程序中，由应用程序提供多个线程执行控制。
> 每个线程都有他自己的一组CPU寄存器，称为线程的上下文，该上下文反映了线程上次运行该线程的CPU寄存器的状态。
> 指令指针和堆栈指针寄存器是线程上下文中两个最重要的寄存器，线程总是在进程得到上下文中运行的，这些地址都用于标志拥有线程的进程地址空间中的内存。
> 线程可以被抢占（中断）。
> 在其他线程正在运行时，线程可以暂时搁置（也称为睡眠） -- 这就是线程的退让。

**Python中使用线程有两种方式：函数或者用类来包装线程对象。**

## 1. 函数 thread.start_new_thread

函数式：调用thread模块中的start_new_thread()函数来产生新线程。语法如下:
> `thread.start_new_thread ( function, args[, kwargs] )`
>> 参数说明:
>>>     function - 线程函数。
>>>     args - 传递给线程函数的参数,他必须是个tuple类型。
>>>     kwargs - 可选参数。

```
# -*- coding: UTF-8 -*-
 
import thread
import time
 
# 为线程定义一个函数
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print "%s: %s" % ( threadName, time.ctime(time.time()) )
 
# 创建两个线程
try:
   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print "Error: unable to start thread"
```
> 线程的结束一般依靠线程函数的自然结束；也可以在线程函数中调用thread.exit()，他抛出SystemExit exception，达到退出线程的目的。


## 2. 线程模块

- thread：多线程的底层支持模块，一般不建议使用；
- threading：对thread进行了封装，将一些线程的操作对象化

> threading模块
>> - Thread 线程类，这是我们用的最多的一个类，你可以指定线程函数执行或者继承自它都可以实现子线程功能；
>> - Timer与Thread类似，但要等待一段时间后才开始运行；
>> - Lock 锁原语，这个我们可以对全局变量互斥时使用；
>> - RLock 可重入锁，使单线程可以再次获得已经获得的锁；
>> - Condition 条件变量，能让一个线程停下来，等待其他线程满足某个“条件”；
>> - Event 通用的条件变量。多个线程可以等待某个事件发生，在事件发生后，所有的线程都被激活；
>> - Semaphore为等待锁的线程提供一个类似“等候室”的结构；
>> - BoundedSemaphore 与semaphore类似，但不允许超过初始值；
>> - Queue：实现了多生产者（Producer）、多消费者（Consumer）的队列，支持锁原语，能够在多个线程之间提供很好的同步支持。


> 其中Thread类
>> - 是你主要的线程类，可以创建进程实例。该类提供的函数包括：
>> - getName(self) 返回线程的名字
>> - isAlive(self) 布尔标志，表示这个线程是否还在运行中
>> - isDaemon(self) 返回线程的daemon标志
>> - join(self, timeout=None) 程序挂起，直到线程结束，如果给出timeout，则最多阻塞timeout秒
>> - run(self) 定义线程的功能函数
>> - setDaemon(self, daemonic) 把线程的daemon标志设为daemonic
>> - setName(self, name) 设置线程的名字
>> - start(self) 开始线程执行

> 其中Queue提供的类
>> - Queue队列
>> - LifoQueue后入先出（LIFO）队列
>> - PriorityQueue 优先队列

> 示例来展示threading的各个功能，包括但不限于：**两种方式起线程、threading.Thread类的重要函数、使用Lock互斥及RLock实现重入锁、使用Condition实现生产者和消费者模型、使用Event和Semaphore多线程通信**


## 3. 创建线程的方式
> 1. 将函数传递进Thread对象: threading.Thread(target=thread_fun, name=thread_name, args=(5,))
> 2. 继承自threading.Thread类: class MyThread(threading.Thread)

## 4. 控制线程
> **将会介绍如何控制这些线程，包括子线程的退出，子线程是否存活及将子线程设置为守护线程(Daemon)。**

1. join方法
> join方法原型如下，这个方法是用来阻塞当前上下文，直至该线程运行结束：
> `def join(self, timeout=None):`
> timeout可以设置超时时间

2. setDaemon方法
```
当我们在程序运行中，执行一个主线程，如果主线程又创建一个子线程，主线程和子线程就分兵两路，
当主线程完成想退出时，会检验子线程是否完成。如果子线程未完成，则主线程会等待子线程完成后再退出。
但是有时候我们需要的是，只要主线程完成了，不管子线程是否完成，都要和主线程一起退出，这时就可以用setDaemon方法，并设置其参数为True。
```

3. 使用Lock互斥锁
> Lock（指令锁）是可用的最低级的同步指令。Lock处于锁定状态时，不被特定的线程拥有。Lock包含两种状态——锁定和非锁定，以及两个基本的方法。
> 可以认为Lock有一个锁定池，当线程请求锁定时，将线程至于池中，直到获得锁定后出池。池中的线程处于状态图中的同步阻塞状态。
> 构造方法： 
>> Lock()
> 实例方法： 
>> acquire([timeout]): 使线程进入同步阻塞状态，尝试获得锁定。 
>> release(): 释放锁。使用前线程必须已获得锁定，否则将抛出异常。

> 现在我们考虑这样一个问题：假设各个线程需要访问同一公共资源，我们的代码该怎么写？

```
import threading
import time
counter = 0

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
 
    def run(self):
        time.sleep(1);
        counter += 1
        print "I am %s, set counter:%s" % (self.name, counter)
 
if __name__ == "__main__":
    for i in range(0, 200):
        my_thread = MyThread()
        my_thread.start()

最后几行输出结果可能为：
I am Thread-193, set counter:189
I am Thread-194, set counter:190
I am Thread-199, set counter:191I am Thread-197, set counter:192
 I am Thread-195, set counter:193I am Thread-196, set counter:196I am Thread-198, set counter:194
I am Thread-200, set counter:195
```
> 从中我们已经看出了这个全局资源(counter)被抢占的情况，
> 问题产生的原因就是没有控制多个线程对同一资源的访问，对数据造成破坏，使得线程运行的结果不可预期。
> 这种现象称为“线程不安全”。在开发过程中我们必须要避免这种情况，那怎么避免？这就用到了我们在综述中提到的互斥锁了。

### 互斥锁概念
> Python编程中，引入了对象互斥锁的概念，来保证共享数据操作的完整性。
> 每个对象都对应于一个可称为” 互斥锁” 的标记，这个标记用来保证在任一时刻，只能有一个线程访问该对象。在Python中我们使用threading模块提供的Lock类。
> 我们对上面的程序进行整改，为此我们需要添加一个互斥锁变量mutex = threading.Lock()，
> 然后在争夺资源的时候之前我们会先抢占这把锁mutex.acquire()，对资源使用完成之后我们在释放这把锁mutex.release()。

```
import threading
import time

counter = 0
mutex = threading.Lock()

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global counter
        time.sleep(1);
        with mutex:
            counter += 1
            print "I am %s, set counter:%s" % (self.name, counter)

if __name__ == "__main__":
    for i in range(0, 200):
        my_thread = MyThread()
        my_thread.start()
```

### 同步阻塞
> 当一个线程调用Lock对象的acquire()方法获得锁时，这把锁就进入“locked”状态。
> 因为每次只有一个线程1可以获得锁，所以如果此时另一个线程2试图获得这个锁，该线程2就会变为“block“同步阻塞状态。
> 直到拥有锁的线程1调用锁的release()方法释放锁之后，该锁进入“unlocked”状态。
> 线程调度程序从处于同步阻塞状态的线程中选择一个来获得锁，并使得该线程进入运行（running）状态。

#### 进一步考虑
> 通过对公共资源使用互斥锁，这样就简单的到达了我们的目的，但是如果我们又遇到下面的情况：
>> 1、遇到锁嵌套的情况该怎么办，这个嵌套是指当我一个线程在获取临界资源时，又需要再次获取；
>> 2、如果有多个公共资源，在线程间共享多个资源的时候，如果两个线程分别占有一部分资源并且同时等待对方的资源；

**上述这两种情况会直接造成程序挂起，即死锁，下面我们会谈死锁及可重入锁RLock。**


#### 死锁的形成
> - 如果有多个公共资源，在线程间共享多个资源的时候，如果两个线程分别占有一部分资源并且同时等待对方的资源，这会引起什么问题？

#### 死锁概念
> 所谓死锁： 
>> 是指两个或两个以上的进程在执行过程中，因争夺资源而造成的一种互相等待的现象，若无外力作用，它们都将无法推进下去。
>> 此时称系统处于死锁状态或系统产生了死锁，这些永远在互相等待的进程称为死锁进程。 
>> 由于资源占用是互斥的，当某个进程提出申请资源后，使得有关进程在无外力协助下，永远分配不到必需的资源而无法继续运行，这就产生了一种特殊现象死锁。

- 代码: [3.Thread.DeadLock.py](https://github.com/yc19890920/python_learn/tree/master/Process-Thread-Coroutine/Thread/3.Thread.DeadLock.py)

代码中展示了一个线程的两个功能函数分别在获取了一个竞争资源之后再次获取另外的竞争资源，运行发现程序已经挂起在那儿了，这种现象我们就称之为”死锁“。


#### 避免死锁
> 避免死锁主要方法就是：正确有序的分配资源，避免死锁算法中最有代表性的算法是Dijkstra E.W 于1968年提出的银行家算法。


## 4. 可重入锁RLock
> RLock（可重入锁）是一个可以被同一个线程请求多次的同步指令。
> RLock使用了“拥有的线程”和“递归等级”的概念，处于锁定状态时，RLock被某个线程拥有。拥有RLock的线程可以再次调用acquire()，释放锁时需要调用release()相同次数。
> 可以认为RLock包含一个锁定池和一个初始值为0的计数器，每次成功调用 acquire()/release()，计数器将+1/-1，为0时锁处于未锁定状态。

> 构造方法： 
>> RLock()

> 实例方法： 
>> acquire([timeout])/release(): 跟Lock差不多。

```
# encoding: UTF-8
import threading
import time
 
rlock = threading.RLock()
 
def func():
    # 第一次请求锁定
    print '%s acquire lock...' % threading.currentThread().getName()
    if rlock.acquire():
        print '%s get the lock.' % threading.currentThread().getName()
        time.sleep(2)
        
        # 第二次请求锁定
        print '%s acquire lock again...' % threading.currentThread().getName()
        if rlock.acquire():
            print '%s get the lock.' % threading.currentThread().getName()
            time.sleep(2)
        
        # 第一次释放锁
        print '%s release lock...' % threading.currentThread().getName()
        rlock.release()
        time.sleep(2)
        
        # 第二次释放锁
        print '%s release lock...' % threading.currentThread().getName()
        rlock.release()
 
t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func)
t3 = threading.Thread(target=func)
t1.start()
t2.start()
t3.start()
```


## 5. 使用Condition实现复杂同步
> Condition（条件变量）通常与一个锁关联。需要在多个Contidion中共享一个锁时，可以传递一个Lock/RLock实例给构造方法，否则它将自己生成一个RLock实例。
> 可以认为，除了Lock带有的锁定池外，Condition还包含一个等待池，池中的线程处于状态图中的等待阻塞状态，直到另一个线程调用notify()/notifyAll()通知；得到通知后线程进入锁定池等待锁定。

> 构造方法： 
>> Condition([lock/rlock])

> 实例方法： 
>> acquire([timeout])/release(): 调用关联的锁的相应方法。 
>> wait([timeout]): 调用这个方法将使线程进入Condition的等待池等待通知，并释放锁。使用前线程必须已获得锁定，否则将抛出异常。 
>> notify(): 调用这个方法将从等待池挑选一个线程并通知，收到通知的线程将自动调用acquire()尝试获得锁定（进入锁定池）；其他线程仍然在等待池中。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。 
>> notifyAll(): 调用这个方法将通知等待池中所有的线程，这些线程都将进入锁定池尝试获得锁定。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。

```
目前我们已经会使用Lock去对公共资源进行互斥访问了，也探讨了同一线程可以使用RLock去重入锁，
但是尽管如此我们只不过才处理了一些程序中简单的同步现象，我们甚至还不能很合理的去解决使用Lock锁带来的死锁问题。
所以我们得学会使用更深层的解决同步问题。
```

> Python提供的Condition对象提供了对复杂线程同步问题的支持。
> Condition被称为条件变量，除了提供与Lock类似的acquire和release方法外，还提供了wait和notify方法。

> 使用Condition的主要方式为：
>> 线程首先acquire一个条件变量，然后判断一些条件。
>> 如果条件不满足则wait；如果条件满足，进行一些处理改变条件后，通过notify方法通知其他线程，其他处于wait状态的线程接到通知后会重新判断条件。
>> 不断的重复这一过程，从而解决复杂的同步问题。

- 生产者-消费者 模型，Condition实现复杂同步
- 代码: [4.Thread.Condition.py](https://github.com/yc19890920/python_learn/tree/master/Process-Thread-Coroutine/Thread/4.Thread.Condition.py)


## Semaphore/BoundedSemaphore
> Semaphore（信号量）是计算机科学史上最古老的同步指令之一。
> Semaphore管理一个内置的计数器，每当调用acquire()时-1，调用release() 时+1。计数器不能小于0；当计数器为0时，acquire()将阻塞线程至同步锁定状态，直到其他线程调用release()。
> 基于这个特点，Semaphore经常用来同步一些有“访客上限”的对象，比如连接池。
> BoundedSemaphore 与 Semaphore 的唯一区别在于前者将在调用release()时检查计数器的值是否超过了计数器的初始值，如果超过了将抛出一个异常。

> 构造方法： 
>> Semaphore(value=1): value是计数器的初始值。

> 实例方法： 
>> acquire([timeout]): 请求Semaphore。如果计数器为0，将阻塞线程至同步阻塞状态；否则将计数器-1并立即返回。 
>> release(): 释放Semaphore，将计数器+1，如果使用BoundedSemaphore，还将进行释放次数检查。release()方法不检查线程是否已获得 Semaphore。


## 7. 使用Event实现线程间通信
> 使用threading.Event可以使一个线程等待其他线程的通知，我们把这个Event传递到线程对象中，Event默认内置了一个标志，初始值为False。
> 一旦该线程通过wait()方法进入等待状态，直到另一个线程调用该Event的set()方法将内置标志设置为True时，该Event会通知所有等待状态的线程恢复运行。

```
Event（事件）是最简单的线程通信机制之一：一个线程通知事件，其他线程等待事件。
Event内置了一个初始为False的标志，当调用set()时设为True，调用clear()时重置为 False。wait()将阻塞线程至等待阻塞状态。
Event其实就是一个简化版的 Condition。Event没有锁，无法使线程进入同步阻塞状态。
```

> 构造方法： 
>> Event()

> 实例方法： 
>> isSet(): 当内置标志为True时返回True。 
>> set(): 将标志设为True，并通知所有处于等待阻塞状态的线程恢复运行状态。 
>> clear(): 将标志设为False。 
>> wait([timeout]): 如果标志为True将立即返回，否则阻塞线程至等待阻塞状态，等待其他线程调用set()。


## 7. Timer
- Timer（定时器）是Thread的派生类，用于在指定时间后调用一个方法。
> 构造方法： 
> Timer(interval, function, args=[], kwargs={}) 
>> interval: 指定的时间 
>> function: 要执行的方法 
>> args/kwargs: 方法的参数

> 实例方法： 
>> Timer从Thread派生，没有增加实例方法。

```
import threading
 
def func():
    print 'hello timer!'
 
timer = threading.Timer(5, func)
timer.start()
```








