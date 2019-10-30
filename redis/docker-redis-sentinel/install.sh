#!/usr/bin/env bash

CURPATH=$(pwd)

function install_redis_image() {
    echo "安装redis镜像.................."
    cd $CURPATH
    # docker build -t redis: .
    # docker build --no-cache -t redis/sential:1 -f Dockerfile .
    docker build -t redis/sentinel:1 -f Dockerfile .
    docker images -a
}

function create_network() {
:<<EOF
Docker 强大的原因之一在于多个 Docker 容器之间的互相连接。涉及到连接，就引出了网络通信的几种模式。Docker 默认提供了 5 种网络驱动模式。
bridge: 默认的网络驱动模式。如果不指定驱动程序，bridge 便会作为默认的网络驱动模式。当应用程序运行在需要通信的独立容器 (standalone containers) 中时，通常会选择 bridge 模式。
host：移除容器和 Docker 宿主机之间的网络隔离，并直接使用主机的网络。host 模式仅适用于 Docker 17.06+。
overlay：overlay 网络将多个 Docker 守护进程连接在一起，并使集群服务能够相互通信。您还可以使用 overlay 网络来实现 swarm 集群和独立容器之间的通信，或者不同 Docker 守护进程上的两个独立容器之间的通信。该策略实现了在这些容器之间进行操作系统级别路由的需求。
macvlan：Macvlan 网络允许为容器分配 MAC 地址，使其显示为网络上的物理设备。 Docker 守护进程通过其 MAC 地址将流量路由到容器。对于希望直连到物理网络的传统应用程序而言，使用 macvlan 模式一般是最佳选择，而不应该通过 Docker 宿主机的网络进行路由。
none：对于此容器，禁用所有联网。通常与自定义网络驱动程序一起使用。none 模式不适用于集群服务。

还可以采用其他一些选项，比如 --subnet、--gateway和 --ip-range。可以使用 docker network – help或 docker network [COMMAND] – help命令查看更多信息。

EOF

    echo "安装docker网络：172.60.0.0/16 .................."
    docker network create --subnet=172.60.0.0/16 redis-network
    docker network ls
}


function create_redis() {
:<<EOF
-d: 后台运行容器，并返回容器ID；
-i: 以交互模式运行容器，通常与 -t 同时使用；
-p: 端口映射，格式为：主机(宿主)端口:容器端口
-t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；
--ip: 为容器制定一个固定的ip
--net: 指定网络模式

EOF

# docker exec -it redis-master bash
echo "安装docker redis 主从.................."
mkdir -vp $(pwd)/redis/{data,data1,data2,data3,log,log1,log2,log3}

docker run \
    --net redis-network \
    --ip 172.60.0.2 \
    -p 6382:6379 \
    -v $(pwd)/redis/data:/var/lib/redis \
    -v $(pwd)/redis/log:/var/log/redis \
    --restart=always \
    --privileged=true \
    --name Redis-master \
    -d redis/sentinel:1 \
    redis-server /config/redis-master.conf --appendonly yes

docker run \
    --net redis-network \
    --ip 172.60.0.3 \
    -p 6383:6379 \
    -v $(pwd)/redis/data1:/var/lib/redis \
    -v $(pwd)/redis/log1:/var/log/redis \
    --restart=always \
    --privileged=true \
    --name Redis-slave-1 \
    -d redis/sentinel:1 \
    redis-server /config/redis-slave.conf --appendonly yes

docker run \
    --net redis-network \
    --ip 172.60.0.4 \
    -p 6384:6379 \
    -v $(pwd)/redis/data2:/var/lib/redis \
    -v $(pwd)/redis/log2:/var/log/redis \
    --restart=always \
    --privileged=true \
    --name Redis-slave-2 \
    -d redis/sentinel:1 \
    redis-server /config/redis-slave.conf --appendonly yes

docker run \
    --net redis-network \
    --ip 172.60.0.5 \
    -p 6385:6379 \
    -v $(pwd)/redis/data3:/var/lib/redis \
    -v $(pwd)/redis/log3:/var/log/redis \
    --restart=always \
    --privileged=true \
    --name Redis-slave-3 \
    -d redis/sentinel:1 \
    redis-server /config/redis-slave.conf --appendonly yes

}

function create_redis_sentinel() {
    echo "安装docker redis sentinel.................."
mkdir -vp $(pwd)/redis/{log-sentinel,log-sentinel1,log-sentinel2,log-sentinel3}

docker run \
    --net redis-network \
    --ip 172.60.0.6 \
    -p 26382:26379 \
    -v $(pwd)/redis/log-sentinel:/var/log/redis \
    --restart=always \
    --name Redis-sentinel-1 \
    -d redis/sentinel:1 \
    redis-sentinel /config/redis-sentinel.conf

docker run \
    --net redis-network \
    --ip 172.60.0.7 \
    -p 26383:26379 \
    -v $(pwd)/redis/log-sentinel1:/var/log/redis \
    --restart=always \
    --name Redis-sentinel-2 \
    -d redis/sentinel:1 \
    redis-sentinel /config/redis-sentinel.conf

docker run \
    --net redis-network \
    --ip 172.60.0.8 \
    -p 26384:26379 \
    -v $(pwd)/redis/log-sentinel2:/var/log/redis \
    --restart=always \
    --name Redis-sentinel-3 \
    -d redis/sentinel:1 \
    redis-sentinel /config/redis-sentinel.conf

docker run \
    --net redis-network \
    --ip 172.60.0.9 \
    -p 26385:26379 \
    -v $(pwd)/redis/log-sentinel3:/var/log/redis \
    --restart=always \
    --name Redis-sentinel-4 \
    -d redis/sentinel:1 \
    redis-sentinel /config/redis-sentinel.conf
}
function check_status() {
    sleep 2;
    ehco "查看状态.................."
    docker ps -a
}

install_redis_image;
create_network;
create_redis;
create_redis_sentinel;
check_status;


