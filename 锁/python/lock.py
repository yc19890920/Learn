# -*- coding: utf-8 -*- 
"""
Author：     yangcheng
date：       2019/11/22 9:44
Description：

"""

# 需要注意的是，lock.acquire() 和 lock.release()必须成对出现。否则就有可能造成死锁。
import threading

# 生成锁对象，全局唯一
lock = threading.Lock()

# 获取锁。未获取到会阻塞程序，直到获取到锁才会往下执行
lock.acquire()

# 释放锁，归回倘，其他人可以拿去用了
lock.release()