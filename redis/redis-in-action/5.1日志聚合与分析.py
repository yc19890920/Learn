# -*- coding: utf-8 -*-
"""
对日志进行聚合运算 或者对页面浏览量进行分析的时候，我们唯一需要考虑的就是：
如果redis因为崩溃而未能成功创建的快照，那么我们能够承受丢失多长时间以内产生的新数据。
如果丢失一个小时之内产生的数据是被允许的，那么可以设置配置save 3600 1。在决定好了持久化配置值之后，
另一个需要解决的问题就是如何恢复因为故障而被中断的日志处理操作。
"""
import os
import redis

def process_logs(redis, path, callback):
    """ 处理日志文件的同时，记录被处理日志文件的名字和偏移量
    :param redis:  Redis 连接
    :param path:   存储日志文件的路径
    :param callback: 待处理日志文件中各个行（line）的回调函数（callback）
    :return:
    """
    # 获取当前文件当前的处理进度
    current_file, offeset = redis.mget("progress:file",  "progress:position")

    pipe = redis.pipeline()
    # 通过调用闭包来减少重复代码
    # 更新正在处理的日志文件名字和偏移量
    def update_progress():
        pipe.mset({
            "progress:file": fname,
            "progress:position": offeset,
        })
        pipe.execute()

    # 有序的遍历各个日志文件
    for fname in sorted(os.listdir(path)):
        # 略过所有已处理的日志文件
        if fname < current_file:
            continue

        # 再接着处理一个因为系统崩溃而未能完成处理的日志文件时，略过已处理的内容。
        inp = open(os.path.join(path, fname), 'rb')
        if fname == current_file:
            inp.seek(int(offeset, 10))
        else:
            offeset = 0

        current_file = None
        # 处理日志
        for lno, line in enumerate(inp):
            # 处理日志行
            callback(pipe, line)
            offeset += int(offeset) + len(line)
            if not (lno+1)%1000:
                # 每当处理完1000个日志行或者处理完整个日志文件的时候，都更新一次文件的处理进度。
                update_progress()
        update_progress()
        inp.close()




