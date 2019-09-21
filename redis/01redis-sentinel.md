- [redis一主二从三哨兵](https://my.oschina.net/wangxu3655/blog/2214310)

## 环境准备
三台独立的linux主机
内网IP分别为: 172.31.175.142、172.31.175.143、172.31.175.144
分别创建带主目录的普通用户, 比如 useradd wx -m

## 安装redis
分别在各个主机上安装redis,以172.31.175.142为例,步骤如下
```
#下载4.0稳定版
wget http://download.redis.io/releases/redis-4.0.11.tar.gz
#解压到用户主目录
tar -xzvf redis-4.0.11.tar.gz -C /home/wx
#进入用户主目录
cd /home/wx
#重命名解压的文件
mv redis-4.0.11 redis
#进入redis目录
cd redis
#编译
make 
#安装,PREFIX指定安装路径
make PREFIX=/home/wx/redis install
```

## 主从/哨兵配置
一主(master)二从(slave)三哨兵(sentinel)的配置目标, 如下:
![img/01一主(master)二从(slave)三哨兵(sentinel).jpg](01一主(master)二从(slave)三哨兵(sentinel).jpg)

redis.conf 配置主从, sentinel.conf 配置哨兵

conf 里面很多初始的配置项可以不做修改, 对于需要修改或新增的配置项, 说明如下

- 通用配置
下面3项,务必在每个 redis.conf 里进行修改,在每个 sentinel.conf 里新增(默认没有)
```
#支持内网/本地访问,比如 bind 172.31.175.142 127.0.0.1
bind 本机内网IP 127.0.0.1
# 支持后台运行,默认值为no
daemonize yes
# 日志文件,比如redis.log、sentinel.log
logfile xxx.log
```

- slave的配置
在2个slave的redis.conf下指定master
```
#指定master
slaveof 172.31.175.142 6379
```

- sentinel的配置
在3个 sentinel.conf 下指定监控的master
```
#指定监控的master,最后一位表示quorum(法人数量),即认定master'客观下线'成立的最低票数
sentinel monitor mymaster 172.31.175.142 6379 2
```

## 主从/哨兵运行
分别启动主从redis, 验证没问题,再分别启动哨兵,假设已进入redis/bin目录

- 运行redis
1, 启动redis
./redis-server ../redis.conf

2, 查看日志
tail -100f ../redis.log 

3, 连接redis
./redis-cli

4, 查看主从信息
cli连接redis成功后, 输入 info replication
![img/01master.jpg](01master.jpg)

下面是其中一个slave的replication信息
![img/01slave.jpg](01slave.jpg)

5, 测试主从同步
在master上写入变量, 在slave上查看是否同步, 此过程略.

-  运行哨兵
```
./redis-sentinel  ../sentinel.conf
```

一个哨兵的日志如下, 可以看出哨兵正在监听,并已识别到2个slave
![img/01sentinel.jpg](01sentinel.jpg)

## 故障转移
模拟发生故障, 进入master主机172.31.175.142, kill掉redis-server进程.
接下来, 查看各个哨兵的日志, 大抵可以看出哨兵的工作过程, 如下

1, 主观下线(sdown)
当某个哨兵心跳检测master超时后,则认定其sdown
+sdown master mymaster 172.31.175.142 6379

2, 客观下线(odown)
当认定sdown的哨兵数>=quorum时,则master下线事实最终成立,即odown
 +odown master mymaster 172.31.175.142 6379 #quorum 2/2

3, 选举哨兵leader
各哨兵协商,选举出一个leader,由其进行故障转移操作
+vote-for-leader 1dd7873228b4bf30c1668d55a28b3036072ee9de 1

4, 故障转移
选择一个slave作为新的master, 并将其他节点设置为新master的slave (刚才已下线的老master的配置文件也会被设置slaveof...) 
+switch-master mymaster 172.31.175.142 6379 172.31.175.144 6379

当故障转移成功后, redis就是一主一从, 如下

主机|角色
--|--:
172.31.175.142 | 哨兵、master
172.31.175.143 | 哨兵、slave
172.31.175.144 | 哨兵、slave -> master

![img/01failover.jpg](01failover.jpg)

进入新的master 172.31.175.144, 查看redis的主从信息, 还剩一从172.31.175.143
![img/01failover2.jpg](01failover2.jpg)

## 故障恢复
模拟故障恢复,进入老的master 172.31.175.142, 重启刚才kill掉的redis, 之后查看其主从信息, 发现老的master已经变成slave了,如下
![img/01recovery.jpg](01recovery.jpg)

//因为172.31.175.142的redis.conf在故障转移时被修改了,所以重启之后就直接成了slave
进入新的master 172.31.175.144下,再去查看最新的主从信息, 发现加入了新的slave, 如下
![img/01recovery2.jpg](01recovery2.jpg)


故障恢复之后, redis恢复到了一主二从三哨兵, 只不过master/slave换了地方, 如下
![img/01recovery3.jpg](01recovery3.jpg)

//若此时想要调整master/slave, 则需要手工操作, 所以为了方便起见, 建议在故障转移之前备份配置文件.
