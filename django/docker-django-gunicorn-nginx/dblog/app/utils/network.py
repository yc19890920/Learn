# -*- coding: utf-8 -*-

import psutil
def get_nets():
    return psutil.net_io_counters(pernic=True).keys()  # 获取网卡名称

def get_nets_io(nets=None):
    if not nets:
        key_info = get_nets()  # 获取网卡名称
    recv = {}
    sent = {}
    for key in key_info:
        recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)  # 各网卡接收的字节数
        sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)  # 各网卡发送的字节数
    return key_info, recv, sent

def get_nets_io_rate(func):
    import time

    key_info, old_recv, old_sent = func()  # 上一秒收集的数据

    time.sleep(1)

    key_info, now_recv, now_sent = func()  # 当前所收集的数据

    net_in = {}
    net_out = {}

    for key in key_info:
        net_in.setdefault(key, now_recv.get(key) - old_recv.get(key))  # 每秒接收速率
        net_out.setdefault(key, now_sent.get(key) - old_sent.get(key))  # 每秒发送速率
        # net_in.setdefault(key, round(((now_recv.get(key) - old_recv.get(key)) / 1024), 2))  # 每秒接收速率
        # net_out.setdefault(key, round(((now_sent.get(key) - old_sent.get(key)) / 1024), 2))  # 每秒发送速率

    return key_info, net_in, net_out

def trans_io(num, unit=1024, places=2):
    return round( float(num) / float(unit), places )

if __name__ == "__main__":
    key_info, net_in, net_out = get_nets_io_rate(get_nets_io)
    # print('-----------------------', key_info, net_in, net_out)
    # ['vethed8bd96', 'veth07d0c4d', 'docker0', 'veth22fa1dd', 'veth1e14688', 'ens160', 'veth03abfca', 'vethaf7fd5b',
    #  'veth63f726b', 'lo', 'veth88bc1b4', 'br-ed615a0f409e']
    # {'vethed8bd96': 0.0, 'veth07d0c4d': 3.0, 'docker0': 0.0,
    #  'veth22fa1dd': 1.0, 'veth1e14688': 0.0, 'ens160': 6.0,
    #  'veth03abfca': 0.0, 'vethaf7fd5b': 0.0,
    #  'veth63f726b': 0.0, 'lo': 0.0, 'veth88bc1b4': 0.0,
    #  'br-ed615a0f409e': 0.0}
    # {'vethed8bd96': 0.0,
    #  'veth07d0c4d': 1.0,
    #  'docker0': 0.0,
    #  'veth22fa1dd': 3.0,
    #  'veth1e14688': 0.0,
    #  'ens160': 3.0,
    #  'veth03abfca': 0.0,
    #  'vethaf7fd5b': 0.0,
    #  'veth63f726b': 0.0, 'lo': 0.0,
    #  'veth88bc1b4': 0.0,
    #  'br-ed615a0f409e': 0.0}
    # while 1:
    #     try:
    #         key_info, net_in, net_out = get_nets_io_rate(get_nets_io)
    #
    #         for key in key_info:
    #             print('%s\nInput:\t %-5sKB/s\nOutput:\t %-5sKB/s\n' % (key, net_in.get(key), net_out.get(key)))
    #     except KeyboardInterrupt:
    #         exit()