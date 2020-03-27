import gevent.monkey
gevent.monkey.patch_all()

import gevent
import gevent.pool
import functools
from collections import defaultdict
try:
    from gevent.coros import BoundedSemaphore
except:
    from gevent.lock import BoundedSemaphore
sem = BoundedSemaphore(1)

def gevent_lock(sem):
    def lock(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with sem:
                return func(*args, **kwargs)
        return wrapper
    return lock

# NestedDict = lambda: defaultdict(NestedDict)
# print(type(NestedDict))
# nestedD = NestedDict()
# print(nestedD)

DJIP = {
    "202.103.5.5": (2369, 2369, 10),
    "202.103.5.8": (2369, 2369, 10),
    "202.103.5.9": (2589, 2369, 10),
    "202.103.10.9": (5, 1, 100),
    "202.103.2.9": (3, 1, 100),
}

DJEMAIL = {
    "1@qq.com": (2369, 2369, 10),
    "2@qq.com": (3001, 2369, 10),
    "3@163.com": (2589, 2369, 10),
    "8@163.com": (5, 1, 5),
    "9@163.com":  (2, 1, 5),
}

class NewNestedDict(dict):

    def __init__(self):
        super().__init__()

    def get_user(self, ip, email):
        for parent_id in self:
            for user_id in self[parent_id]['users']:
                if (ip, email) in self[parent_id]['users'][user_id]['addrs']:
                    return parent_id, user_id
        return self.add_user(ip, email)

    @gevent_lock(sem)
    def add_user(self, ip, email):
        if ip in DJIP:
            user_id, parent_id, points = DJIP[ip]
        elif email in DJEMAIL:
            user_id, parent_id, points = DJEMAIL[email]
        else:
            return None, None
        addr = (ip, email)
        u = { user_id: {'user_id': user_id, 'parent_id': parent_id,'addrs': [addr] } }
        if parent_id in self:
            if user_id in self[parent_id]['users']:
                self[parent_id]['users'][int(user_id)]['addrs'].append(addr)
            else:
                self[parent_id]['users'].update(u)
        else:
            self.update({ parent_id: { 'points': points, 'users': u } })
        return parent_id, user_id

    @gevent_lock(sem)
    def reduce_points(self, user_id, parent_id, point=1):
        if self[parent_id]['points']<=0:
            return 0
        self[parent_id]['points'] -= point
        return self.get_points(user_id, parent_id)

    def get_points(self, user_id, parent_id):
        return self[parent_id]['points']

    @gevent_lock(sem)
    def remove_user(self, user_id, parent_id):
        print("delete user_id:{},parent_id:{}".format(user_id, parent_id))
        print(self)
        del self[parent_id]
        print(self)

import random
ND = NewNestedDict()
GLB_THREADS = []

def __consumer(ip, email):
    parent_id, user_id = ND.get_user(ip, email)
    if not user_id:
        print("no user")
        return
    print("user_id:",user_id)
    if not ND.reduce_points(user_id, parent_id):
        ND.remove_user(user_id, parent_id)

def consumer():
    pool = gevent.pool.Pool(5)
    while 1:
        if not GLB_THREADS:
            gevent.sleep(0.2)
            continue
        ip, email = GLB_THREADS.pop()
        pool.spawn(__consumer, ip, email)

def product():
    ips = [ "202.103.5.5",
            "202.103.5.8",
            "202.103.5.9",
            "202.103.10.9",
            "202.103.2.9","202.103.2.10",]
    emails = [
        "1@qq.com",
        "2@qq.com",
        "3@163.com",
        "8@163.com",
        "9@163.com",
        "91@163.com",
    ]
    while 1:
        GLB_THREADS.append((random.choice(ips), random.choice(emails)))
        gevent.sleep(0.3)

def main():
    gevent.joinall([
        gevent.spawn(consumer),
        gevent.spawn(product),
    ])

if __name__ == '__main__':
    print("program start...")
    main()
    print("program end...")
