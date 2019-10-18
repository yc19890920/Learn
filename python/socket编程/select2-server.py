# -*- coding: utf-8 -*-
import selectors, socket

# 创建默认的selectors对象
sel = selectors.DefaultSelector()
socket_list = []

# 负责监听“有数据可读”事件的函数
def read(skt, mask):
    try:
        # 读取数据
        data = skt.recv(1024)
        if data:
            # 将读取的数据采用循环向每个socket发送一次
            for s in socket_list:
                s.send(data)  # Hope it won't block
        else:
            # 如果该socket已被对方关闭，关闭该socket，
            # 并从socket_list列表中删除
            print(u'关闭', skt)
            sel.unregister(skt)
            skt.close()
            socket_list.remove(skt)
    # 如果捕捉到异常, 将该socket关闭，并从socket_list列表中删除
    except:
        print(u'关闭', skt)
        sel.unregister(skt)
        skt.close()
        socket_list.remove(skt)


# 负责监听“客户端连接进来”事件的函数
def accept(sock, mask):
    conn, addr = sock.accept()
    # 使用socket_list保存代表客户端的socket
    socket_list.append(conn)
    conn.setblocking(False)
    # 使用sel为conn的EVENT_READ事件注册read监听函数
    sel.register(conn, selectors.EVENT_READ, read)  # ②


sock = socket.socket()
sock.bind(('192.168.1.88', 30000))
sock.listen()
# 设置该socket是非阻塞的
sock.setblocking(False)
# 使用sel为sock的EVENT_READ事件注册accept监听函数
sel.register(sock, selectors.EVENT_READ, accept)  # ①
# 采用死循环不断提取sel的事件
while True:
    events = sel.select()
    for key, mask in events:
        # key的data属性获取为该事件注册的监听函数
        callback = key.data
        # 调用监听函数, key的fileobj属性获取被监听的socket对象
        callback(key.fileobj, mask)