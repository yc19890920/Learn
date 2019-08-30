# def simple_coroutine():
#     print("started...")
#     x = yield
#     print("received:", x)
#
# c = simple_coroutine()
# print(c)
# next(c)
# # c.send(None)
# c.send(24)


from collections import namedtuple
Result = namedtuple("Result","colunt average")

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count+=1
        average = total/count
    return Result(count,average)

coro_avg = averager()
next(coro_avg)
coro_avg.send(10)
coro_avg.send(30)
coro_avg.send(5)
try:
    coro_avg.send(None)
except StopIteration as e:
    result = e.value
    print(result)

# --------------------------------------
def gen():
    for c in "AB":
        yield c
    for i in range(1,3):
        yield i

print(list(gen()))

def gen2():
    yield from "AB"
    yield from range(1,3)

print(list(gen2()))


# --------------------------------------
def gen3():
    value=0
    while True:
        receive=yield value
        if receive=='e':
            break
        value = 'got: %s' % receive

g=gen3()
print(g.send(None))
print(g.send('hello'))
print(g.send(123456))
print(g.send(None))
print(g.send('e'))


