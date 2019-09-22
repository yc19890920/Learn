docker search rabbitmq
docker pull rabbitmq

## 启动镜像 安装并运行RabbitMQ
使用Docker运行RabbitMQ非常简单，只需要执行一条简单的命令：
docker run -d --name rabbitmq \
    -p 0.0.0.0:10000:5672 \
    -p 0.0.0.0:10001:15672 \
    -v /home/python/data/rabbitmq:/var/lib/rabbitmq \
    --hostname myRabbit \
    -e RABBITMQ_DEFAULT_VHOST=my_vhost  \
    -e RABBITMQ_DEFAULT_USER=admin \
    -e RABBITMQ_DEFAULT_PASS=admin \
    rabbitmq:latest
    
-d : 后台运行容器
--name rabbitmq : 将容器的名字设为rabbitmq
-h rabbitmq : 将容器的主机名设为rabbitmq，希望RabbitMQ消息数据持久化保存到本地磁盘是需要设置主机名，因为RabbitMQ保存数据的目录为主机名
-p 5672:5672 : 将容器的5672端口映射为本地主机的5672端口，这样可以通过本地的5672端口访问rabbitmq
-v /home/python/data/rabbitmq:/var/lib/rabbitmq：将容器的/var/lib/rabbitmq目录映射为本地主机的/var/lib/rabbitmq目录，这样可以将RabbitMQ消息数据持久化保存到本地磁盘，即使RabbitMQ容器被删除，数据依然还在。
-p 指定服务运行的端口（5672：应用访问端口；15672：控制台Web端口号）；
-v 映射目录或文件；
--hostname  主机名（RabbitMQ的一个重要注意事项是它根据所谓的 “节点名称” 存储数据，默认为主机名）；
-e 指定环境变量；（RABBITMQ_DEFAULT_VHOST：默认虚拟机名；RABBITMQ_DEFAULT_USER：默认的用户名；RABBITMQ_DEFAULT_PASS：默认用户名的密码）

## 参数解释：
15672 ：表示 RabbitMQ 控制台端口号，可以在浏览器中通过控制台来执行 RabbitMQ 的相关操作。
5672 : 表示 RabbitMQ 所监听的 TCP 端口号，应用程序可通过该端口与 RabbitMQ 建立 TCP 连接，完成后续的异步消息通信
RABBITMQ_DEFAULT_USER：用于设置登陆控制台的用户名，这里我设置 admin
RABBITMQ_DEFAULT_PASS：用于设置登陆控制台的密码，这里我设置 admin
容器启动成功后，可以在浏览器输入地址：http://ip:15672/ 访问控制台
我的服务器是阿里云服务器，所以还需要去开放一下端口，否则是无法访问的。
这里有一个很重要的问题：RabbitMQ出于安全的考虑，默认是只能访问localhost:15762访问的，如果想用其他ip，是需要自己配置的。


docker exec -it rabbitmq /bin/bash
cd etc/rabbitmq/
vim rabbitmq.config
{rabbit,[{tcp_listeners,[5672]},{loopback_users,["admin"]}]}
rabbitmqctl add_user admin admin
rabbitmqctl set_permissions -p "/" admin ".*" ".*" ".*"
rabbitmqctl set_user_tags admin administrator
rabbitmqctl list_users
rabbitmqctl list_permissions -p /

3.3查看rabbitmq运行状况：
docker logs rabbit


## 安装管理界面
进入docker
docker exec -it rabbitmq /bin/bash
执行
rabbitmq-plugins enable rabbitmq_management
重启
service rabbitmq-server restart


```
启动监控管理器：rabbitmq-plugins enable rabbitmq_management
关闭监控管理器：rabbitmq-plugins disable rabbitmq_management
启动rabbitmq：rabbitmq-service start
关闭rabbitmq：rabbitmq-service stop
查看所有的队列：rabbitmqctl list_queues
清除所有的队列：rabbitmqctl reset
关闭应用：rabbitmqctl stop_app
启动应用：rabbitmqctl start_app
用户和权限设置（后面用处）
 
添加用户：rabbitmqctl add_user username password
分配角色：rabbitmqctl set_user_tags username administrator
新增虚拟主机：rabbitmqctl add_vhost  vhost_name
将新虚拟主机授权给新用户：rabbitmqctl set_permissions -p vhost_name username '.*' '.*' '.*'
角色说明
 
none  最小权限角色
management 管理员角色
policymaker   决策者
monitoring  监控
administrator  超级管理员 
```








