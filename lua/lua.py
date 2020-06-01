"""
Redis 内置的 Lua 解释器加载了以下 Lua 库：
base
table
string
math
debug
cjson
cmsgpack
其中 cjson 库可以让 Lua 以非常快的速度处理 JSON 数据，除此之外，其他别的都是 Lua 的标准库。
"""

import time
import uuid
import math
import random
import redis

connect = redis.Redis()


class FrequencyRequest:
    _digest = None
    __lua__ = """
    local key = KEYS[1]
    -- field: 用户名和IP
    -- expire: 距离当前时间的过期时间间隔
    -- now: 当前时间戳
    local field, expire, now, count, is_set, is_expire = ARGV[1], tonumber(ARGV[2]), tonumber(ARGV[3]), tonumber(ARGV[4]), tonumber(ARGV[5]), tonumber(ARGV[6])

    -- a：历史time cjson字符串
    -- j: 历史time table
    -- b: 当前time集合
    local a, j, b
    a = redis.call('hget', key, field)
    b = {}
    if a then
        j = cjson.decode(a)
        if now >= j[#j] + expire then
                    redis.call('hdel', key, field)
        else
            for i, t in ipairs(j) do
                if tonumber(t) >= now - expire then
                    table.insert(b, t)
                end
            end
        end
    end

    if is_set == 1 then
        -- 删除第一个元素
        if (#b >= count) then
            table.remove(b, 1)
        end

        table.insert(b, now)
        redis.call('hset', key, field, cjson.encode(b))
    end

    -- 设置过期
    if is_expire == 1 then
        redis.call('expire', key, 3600)
    end

    -- 和table时间长度比较
    if (#b >= count) then
        return true
    end
        return false
    """

    @classmethod
    def is_overfreq(cls,
                    key="frequency_request",
                    field="admin-192.168.1.24",
                    count=10, expire=300, is_set=1, is_expire=1, connect=None):
        """ 过频检测，或 登录错误次数检测等
        :param key:
        :param field:    关键字
        :param count:    最大数量
        :param expire:   过期时间
        :param is_set:   1 设置值， 2 获取值  3 删除 field （不使用）
        :param is_expire:   1 key 可以过期，默认以天数过期
        :return:
        """
        if not connect:
            connect = redis.Redis()
        if not cls._digest:
            cls._digest = connect.script_load(cls.__lua__)
        return bool(
            connect.evalsha(cls._digest, 1, *[key, field, expire, time.time(), count, is_set, is_expire])
        )


class OrderRefundExceed:
    _digest = None
    __lua__ = """
    local key, account_id, length, refund, timeout = KEYS[1], ARGV[1], tonumber(ARGV[2]), tonumber(ARGV[3]), tonumber(ARGV[4])
    local cnt, ttl

    -- 统计当前账户 order_id 增量
    cnt = tonumber(redis.call('hget', key, account_id))
    cnt = tonumber((cnt and {cnt} or {0})[1])

    -- 设置过期时间
    redis.call('expire', key, timeout)
    -- 当前账户 order_id 增量大于 refund
    if ( cnt + length > refund ) then
        return {true, refund}
    end

    -- 设置增量
    redis.call('hincrby', key, account_id, length)
    redis.call('expire', key, timeout)
    return {false, refund}
    """

    @classmethod
    def is_exceed(cls, redis, key, account_id, length, refund=30, timeout=24 * 3600):
        """ 实时订单 退款次数过多
        acckey, account_id, llen = "aa", 1, 20
        x = order_refund_exceed(redis, acckey, account_id, llen, refund=30, timeout=24*3600)
        print(x) 返回 [1, 30](已超过) 或者 [None, 50]
        :param redis:
        :param key:           统计当前账户 order_id 增量
        :param account_id:    当前账户
        :param length:        order_id 数量
        :param refund:        一个账户一天可以退款的order_id数量
        :param timeout:       key超时时间
        :return:
        """
        if not cls._digest:
            cls._digest = redis.script_load(cls.__lua__)
        return redis.evalsha(cls._digest, 1, *[key, account_id, length, refund, timeout])


class Locker:
    _acquire_digest = None
    __acquire_lua__ = """
    local key, identify, timeout = KEYS[1], ARGV[1], tonumber(ARGV[2])
    local ident, ret

    ident = redis.call('GET', key)
    if not ident then
        --  设置过期时间锁
        redis.call('SET', key, identify)
        redis.call('EXPIRE', key, timeout)
        ret = identify
    else
        --  未过期时间，则增加过期时间
        if redis.call('ttl', key) < 0 then
            redis.call('expire', key, timeout)
        end
        ret = nil
    end
    return ret
    """
    _release_digest = None
    __release_lua__ = """
    if redis.call('get', KEYS[1]) == ARGV[1] then
        return redis.call('del', KEYS[1]) or true
    end
    """

    @classmethod
    def acquire(cls, redis, lockname, lock_timeout=30):
        identify = str(uuid.uuid4())
        lockname = 'lock:' + lockname
        # 确保传给EXPIRE的都是整数
        lock_timeout = int(math.ceil(lock_timeout))
        if not cls._acquire_digest:
            cls._acquire_digest = redis.script_load(cls.__acquire_lua__)
        return redis.evalsha(cls._acquire_digest, 1, *[lockname, identify, lock_timeout])

    @classmethod
    def release(cls, redis, lockname, identify):
        if not cls._release_digest:
            cls._release_digest = redis.script_load(cls.__release_lua__)
        return bool(
            redis.evalsha(cls._release_digest, 1, *["lock:" + lockname, identify])
        )

    @classmethod
    def release_force(cls, redis, lockname):
        lockname = "lock:" + lockname
        return redis.delete(lockname)


class Graber:
    _digest = None
    __lua__ = """
    local srckey, dstkey = KEYS[1], KEYS[2], KEYS[3]
    local user_id = tonumber(ARGV[1])
    local money

    -- 已抢过红包
    if redis.call('hexists', dstkey, user_id) == 1 then
        return {true, 0}
    end

    -- 未抢到红包
    money = redis.call('rpop', srckey)
    if not money then
        return {false, 0}
    end

    -- 抢到红包
    redis.call('hset', dstkey, user_id, money)
    return {true, tonumber(money)}
    """

    @classmethod
    def grab(cls, redis, srckey, userkey, user_id):
        """
        数据库锁定一部分金额记录， 数据字段： account_id, uuid(主键)，money（分配总金额），expire_at(过期时间), created_at, updated_at，is_expire(过期处理成功标记)
        同时定时任务去最终维护客户实际分配的红包金额，记录哪些人抢了这些红包，分别多少金额, 以及记录运气王
        Lua脚本结合Redis实现抢红包场景
            主要是利用了Redis+lua脚本的原子性。避免出现同一个用户抢两次的情况。
            前提：用户发起红包时，按个数分配好金额，而不是抢的时候再分配。分配结束后存入redis的list中。
            基本思路：两个list1（未分配的红包），list2（分配后的红包） 和一个set。利用set里的key不能重复用来判断用户是否已抢。
            一个Lua脚本下实现三个操作，保证原子性。1：从set中取用户id，判断是否已抢，不存在id，进入步骤2。2：从list1中pop移除一个红包。3：往list2中push一个红包和抢到的用户id。
            最后业务系统来读取分配后的list2信息即可
        :param srckey:   未分配的红包
        :param dstkey:   分配后的红包（用户已抢红包，并记录金额）
        :param user_id:  用户
        :return:
        """
        if not cls._digest:
            cls._digest = redis.script_load(cls.__lua__)
        return redis.evalsha(cls._digest, 2, *[srckey, userkey, user_id])

    @classmethod
    def gen(cls, redis, srckey, money, num, cond=2, is_random=True):
        """ 生成红包
        :param redis:
        :param srckey:
        :param money:  总金额，份数，调控参数（调控平均差）
        :param num:    份数
        :param cond:   调控参数（调控平均差）
        :param is_random:   随机分配
        :return:
        """
        assert type(num) == type(1)
        lst = cls.split(money, num, cond=cond, is_random=is_random)
        p = redis.pipeline()
        p.lpush(srckey, *lst)
        p.expire(srckey, 24 * 3600)
        p.execute()

    @classmethod
    def split(cls, total, num, cond=2, is_random=True):
        """
        # 总金额，份数，调控参数（调控平均差）
        roll(10, 20, 2)
        :param total:  总金额，份数，调控参数（调控平均差）
        :param num:    份数
        :param cond:   调控参数（调控平均差）
        :param is_random:   随机分配
        :return:
        """
        # print("===红包算法研究程序===")
        # print("共", total, "元钱。分", num, "份。条件参数为：", cond)
        if is_random:
            total *= 100
            p = []
            average = total / num
            ##        print "前置平均数",average
            pre = []
            allpre = 0.0
            for count in range(0, num):
                tp = random.randint(1, 10 ** cond)
                pre.append(tp)
                allpre += tp
            ##        print "预备随机序列",pre,len(pre)
            ##        print "预备总数",allpre
            onepre = round(total / allpre, cond)
            ##
            ##        print "预备单份额",onepre
            ##        print "预备总金额",onepre * allpre
            # print('-------')
            alltp = 0
            for m in range(0, len(pre) - 1):
                tp = int(onepre * pre[m])
                if (0 == tp):
                    tp = 1
                alltp += tp
                p.append(tp / 100.0)
            last = total - alltp
            p.append(last / 100.0)
            alltp += last
            # 打乱序列
            random.shuffle(p)
            return p
            # # p.sort()
            # # sorted(p)[0]
            # print("运气王:", sorted(p)[num - 1])  # ,p[num-1]
            # # random.shuffle(p)
            # print("红包序列", p, len(p))
            # print("总共发出", alltp / 100.0)
            # # random.shuffle(p)      # 打乱序列
        else:
            average = round(total / num, cond)
            assert average * num == total
            return [average] * num

    @classmethod
    def left(cls, redis, userkey, money, cond=2):
        """ 剩余金额
        :param redis:
        :param userkey:
        :param money:
        :return:
        """
        t = redis.hgetall(userkey)
        used = round(sum(map(float, t.values())), cond)
        left = round(money - used, cond)
        return left

    @classmethod
    def top(cls, redis, userkey):
        """ 运气王（过期时间内查询）
        :param redis:
        :param userkey:
        :param cond:
        :return:
        """
        t = redis.hgetall(userkey)
        lst = map(lambda x: (int(x[0]), float(x[1])), t.items())
        lst = sorted(lst, key=lambda x: x[1])
        return lst[-1]


def test():
    # ret = FrequencyRequest.is_overfreq(connect=connect, is_set=1)
    # print(ret)

    identify = Locker.acquire(connect, "aa")
    print(identify)
    if identify:
        ret = Locker.release(connect, "aa", identify)
        print(ret)


def test1():
    import uuid
    uuids = str(uuid.uuid4())
    srckey = f"graber:{uuids}"
    userkey = f"graber:user:{uuids}"
    print(srckey, userkey)
    money = 60
    num = 10
    Graber.gen(connect, srckey, money, num, cond=2, is_random=True)
    for __ in range(20):
        user_id = random.randint(1, 5)
        ret = Graber.grab(connect, srckey, userkey, user_id)
        print(user_id, ret, len(ret))
    left = Graber.left(connect, userkey, money, cond=2)
    print(left)

    top = Graber.top(connect, userkey)
    print(top)


if __name__ == '__main__':
    test1()
    # import timeit
    # print(timeit.timeit("test()", setup="from __main__ import test", number=10))
