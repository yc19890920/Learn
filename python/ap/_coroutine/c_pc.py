def consumer():       # 有yield的函数就是生成器，没的跑
    r = 'what the fuck?'
    print(r)   # 😄发送None时，函数从头开始执行的，到 yield r 停止，此后的send(xxx)都是从 n = yield 开始。记住，n = yield 是启动点， yield r 暂停点，并返回yield r结果给produce函数
    while True:
        # 注意，yield r 是代码终止点，n = yield是启动点，
        # 一个正常的循环♻过程是从 n = yield开始执行，到下面，执行到r ='200k'后，再回到 yield r处暂停，
        # 此时暂停的yield r 应该是经过新的循环，这里没有 for in 函数，但是，r最新的200k就是它的新循环，
        # 所以此时yield r为200k时生成器程序也就是consumer停止，但是，新的yield r 要回给send，send发送消息，也会要求得到消息的结果
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)    #
    n = 0     # 没有上面的c.send，系统报错can't send non-None value to a just-started generator
    while n < 5:   #
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCE R] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)