# -*- coding: utf-8 -*-
import etcd3
#往etcd中存数据
client = etcd3.client(host='192.168.1.24')   #连接etcd
r  = client.put('aaa', 'qweqwe')              #往etcd中存键值
print r
b = client.get('aaa')                        #查看etcd中的键值
print b
vents_iterator, cancel = client.watch('aaa')         #监听etcd中aaa键 是否发生改变，
print vents_iterator, cancel
