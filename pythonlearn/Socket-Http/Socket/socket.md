

## Python 网络编程

## 一. socket模块详解，通过这些基础知识更好的理解网络编程。网络知识的一些介绍

1、socket 是网络连接端点。 

例说：当你的Web浏览器请求www.jb51.net上的主页时(即就是发送HTTP请求)，web浏览器会创建一个
socket对象并命令它去连接www.jb51.net的web服务器主机，web服务器也会对来自的请求在一个socket对象上进行监听。客户端和服
务器端各自使用socket来发送和接收消息。

2、使用过程中，每个socket对象都会绑定到一个特定的IP地址和端口。

IP地址是一个由4个数组成的序列，这4个数均是范围 0~255中的值（例如，220,176,36,76)；
端口数值的取值范围是0~65535。端口数小于1024的都是为众所周知的网络服务所保留的（例如Web服务使用的80端口）；最大的
保留数被存储在socket模块的IPPORT_RESERVED变量中。你也可以为你的程序使用另外的端口数值。
地址127.0.0.1是本机地址；它始终指向当前的计算机。程序可以使用这个地址来连接运行在同一计算机上的其它程序。
域名服务器（DNS）处理名字到IP地址的映射。每个计算机都可以有一个主机名，即使它没有在官方注册。
  
3、协议：

  例如HTTP协议，它是用在Web浏览器与Web服务器之间通信的协议，它是基于TCP协议，而TCP协议又基于IP协议。
当在你自己的两个程序间传送信息的时候，你通常选择TCP或UDP协议。TCP协议在两端间建立一个持续的连接，并且你所发送的信息
有保证的按顺序到达它们的目的地。UDP不建立连接，它的速度快但不可靠。你发送的信息也可能到不了另一端；或它们没有按顺序
到达。有时候一个信息的多个复制到达接收端，即使你只发送了一次。


## 二. socket模块简介

socket通常也称作"套接字"，用于描述IP地址和端口，是一个通信链的句柄，应用程序通常通过"套接字"向网络发出请求或者应答网络请求

socket起源于Unix，而Unix/Linux基本哲学之一就是“一切皆文件”，对于文件用【打开】【读写】【关闭】模式来操作。socket就是该模式的一个实现

socket即是一种特殊的文件，一些socket函数就是对其进行的操作（读/写IO、打开、关闭）

socket和file的区别：

- file模块是针对某个指定文件进行【打开】【读写】【关闭】
- socket模块是针对 服务器端 和 客户端Socket 进行【打开】【读写】【关闭】


### Python 提供了两个级别访问的网络服务：
> - 低级别的网络服务支持基本的 Socket，它提供了标准的 BSD Sockets API，可以访问底层操作系统Socket接口的全部方法。
> - 高级别的网络服务模块 SocketServer， 它提供了服务器中心类，可以简化网络服务器的开发。

### 什么是 Socket?
- Socket又称"套接字"，应用程序通常通过"套接字"向网络发出请求或者应答网络请求，使主机间或者一台计算机上的进程间可以通讯。

### socket()函数
> - Python 中，我们用 socket（）函数来创建套接字，语法格式如下：
> `socket.socket([family[, type[, proto]]])`
> ### 参数
>> - family: 套接字家族, 可以是AF_UNIX或者AF_INET
>> - type: 套接字类型,可以根据是面向连接的还是非连接分为SOCK_STREAM或SOCK_DGRAM
>> - protocol: 协议类型，一般不填默认为0.

### 通信流程

![socket.png](https://github.com/yc19890920/python_learn/blob/master/Socket-Http/Socket/img/socket.png)

**使用socket.socket()创建套接字**
> 创建一个TCP/IP套接字　
>> `tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
> 创建UDP/IP套接字
>> `udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`

### Socket 对象(内建)方法

| 函数 |	描述 |
| --- | --- |
| 服务器端套接字||
| s.bind() 	| 绑定地址（host,port）到套接字， 在AF_INET下,以元组（host,port）的形式表示地址。| 
| s.listen(backlog) 	| 开始TCP监听。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。| 
| s.accept() 	| 被动接受TCP客户端连接,(阻塞式)等待连接的到来| 
| 客户端套接字|| 
| s.connect(addr) 	| 主动初始化TCP服务器连接，。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。| 
| s.connect_ex() | 	connect()函数的扩展版本,出错时返回出错码,而不是抛出异常| 
| 公共用途的套接字函数|| 
| s.recv() 	| 接收TCP数据，数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。| 
| s.send() | 	发送TCP数据，将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。| 
| s.sendall() 	| 完整发送TCP数据，完整发送TCP数据。将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。| 
| s.recvfrom() | 	接收UDP数据，与recv()类似，但返回值是（data,address）。其中data是包含接收数据的字符串，address是发送数据的套接字地址。| 
| s.sendto() 	| 发送UDP数据，将数据发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。| 
| s.close() 	| 关闭套接字| 
| s.getpeername() 	| 返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。| 
| s.getsockname() 	| 返回套接字自己的地址。通常是一个元组(ipaddr,port)| 
| s.setsockopt(level,optname,value) 	| 设置给定套接字选项的值。| 
| s.getsockopt(level,optname[.buflen]) | 	返回套接字选项的值。| 
| s.settimeout(timeout) 	| 设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建套接字时设置，因为它们可能用于连接的操作（如connect()）| 
| s.gettimeout() 	| 返回当前超时期的值，单位是秒，如果没有设置超时期，则返回None。| 
| s.fileno() 	| 返回套接字的文件描述符。| 
| s.setblocking(flag) | 	如果flag为0，则将套接字设为非阻塞模式，否则将套接字设为阻塞模式（默认值）。非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起socket.error异常。| 
| s.makefile() | 	创建一个与该套接字相关连的文件| 

```
    accept() -- accept a connection, returning new socket and client address
    bind(addr) -- bind the socket to a local address
    close() -- close the socket
    connect(addr) -- connect the socket to a remote address
    connect_ex(addr) -- connect, return an error code instead of an exception
    dup() -- return a new socket object identical to the current one [*]
    fileno() -- return underlying file descriptor
    getpeername() -- return remote address [*]
    getsockname() -- return local address
    getsockopt(level, optname[, buflen]) -- get socket options
    gettimeout() -- return timeout or None
    listen(n) -- start listening for incoming connections
    makefile([mode, [bufsize]]) -- return a file object for the socket [*]
    recv(buflen[, flags]) -- receive data
    recv_into(buffer[, nbytes[, flags]]) -- receive data (into a buffer)
    recvfrom(buflen[, flags]) -- receive data and sender's address
    recvfrom_into(buffer[, nbytes, [, flags])
      -- receive data and sender's address (into a buffer)
    sendall(data[, flags]) -- send all data
    send(data[, flags]) -- send data, may not send all of it
    sendto(data[, flags], addr) -- send data to a given address
    setblocking(0 | 1) -- set or clear the blocking I/O flag
    setsockopt(level, optname, value) -- set socket options
    settimeout(None | float) -- set or clear the timeout
    shutdown(how) -- shut down traffic in one or both directions
```


### Python Internet 模块

- 以下列出了 Python 网络编程的一些重要模块：

|协议	| 功能用处	| 端口号	| Python 模块 |
| --- | --- | --- | --- |
| HTTP	| 网页访问	| 80	| httplib, urllib, xmlrpclib| 
| NNTP	| 阅读和张贴新闻文章，俗称为"帖子"	| 119	| nntplib| 
| FTP	| 文件传输	| 20	| ftplib, urllib| 
| SMTP	| 发送邮件	| 25	| smtplib| 
| POP3	| 接收邮件	| 110	| poplib| 
| IMAP4	| 获取邮件	| 143	| imaplib| 
| Telnet	| 命令行	| 23	| telnetlib| 
| Gopher	| 信息查找	| 70	| gopherlib, urllib| 


### TCP socket

### UDP socket

### SocketServer socket