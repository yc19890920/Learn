
## 代理服务器设置

- [使用CentOS7配置Squid代理](http://www.cnblogs.com/riversouther/p/4717720.html)
- [CentOS 6.4下Squid代理服务器的安装与配置](http://www.cnblogs.com/mchina/p/centos-squid-proxy-server.html)
- [Squid中文权威指南](http://zyan.cc/book/squid/)
- [五大开源 Web 代理服务器横评：Squid、Privoxy、Varnish、Polipo、Tinyproxy](https://linux.cn/article-7119-1.html)
- [varnish / squid / nginx cache 有什么不同？](https://www.zhihu.com/question/20143441)

```
## 设置 只能某个段IP能访问
## 设置路由， 某个段的IP 可以访问
acl localnet src 202.103.191.0/24       # RFC1918 possible internal network

http_access allow manager localhost
注释掉以下：
#http_access allow all
#http_access deny manager

#http_access deny to_localhost

#http_access deny CONNECT !SSL_ports

#http_access deny !Safe_ports
```

### 1.修改出口IP
>> vim /etc/squid/squid.conf
>> 注释#http_accesS deny all
>> 添加 http_access allow all
```
http_access allow manager localhost
http_access allow all
http_access deny manager
```
>> 定义#define acl
>> `acl myip231 myip 211.159.65.231`
>> 定义# set up outgoing rule
>> `tcp_outgoing_address 211.159.65.231 myip231`

### 2.打开防火墙
vi /etc/sysconfig/iptables

```
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [8:856]
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 88 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 10001 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
```

添加了此行
`-A INPUT -p tcp -m state --state NEW -m tcp --dport 88 -j ACCEPT`

/etc/init.d/squid restart
/etc/init.d/iptables restart

