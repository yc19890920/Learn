## Fanout Exchange – 不处理路由键。
你只需要简单的将队列绑定到交换机上。
一个发送到交换机的消息都会被转发到与该交换机绑定的所有队列上。
很像子网广播，每台子网内的主机都获得了一份复制的消息。Fanout交换机转发消息是最快的。 

## Direct Exchange – 处理路由键。
需要将一个队列绑定到交换机上，要求该消息与一个特定的路由键完全匹配。
这是一个完整的匹配：
如果一个队列绑定到该交换机上要求路由键 “dog”，则只有被标记为“dog”的消息才被转发，不会转发dog.puppy，也不会转发dog.guard，只会转发dog。 

## Topic Exchange – 将路由键和某模式进行匹配。
此时队列需要绑定要一个模式上。
符号“#”匹配一个或多个词，符号“*”匹配不多不少一个词。
因此“audit.#”能够匹配到“audit.irs.corporate”，
但是“audit.*” 只会匹配到“audit.irs”。
我在RedHat的朋友做了一张不错的图，来表明topic交换机是如何工作的： 


## RabbitMQ 命令介绍
1. /etc/init.d/rabbitmq-server start|stop|restart|reload
2. rabbitmq-server add_vhost vhostname  创建Vhost
3. rabbitmq-server delete_vhost vhostname  删除Vhost
4. rabbitmqctl list_vhosts 遍历所有虚拟主机信息
5. rabbitmqctl add_user username password  添加用户名及密码
6. rabbitmqctl change_password username newpassword  修改用户密码
7. rabbitmqctl set_permissions -p v_host user ".*" ".*" ".*"   // 绑定权限，并且具备读写的权限
8. rabbitmqctl list_queues   显式所有队列

```
进入docker
docker exec -it rabbitmq /bin/bash

docker exec rabbitmq   rabbitmqctl list_vhosts
docker exec rabbitmq   rabbitmqctl list_queues

docker exec rabbitmq   rabbitmq-server add_vhost vhostname-test
docker exec rabbitmq   rabbitmq-server delete_vhost vhostname-test

docker exec rabbitmq   rabbitmqctl add_user yc 123456
docker exec rabbitmq   rabbitmqctl set_permissions -p my_vhost yc ".*" ".*" ".*"
```


