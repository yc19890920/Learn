#!/usr/bin/env bash

mkdir -p $(pwd)/data
#chmod 777 data

#docker network ls | grep 'mynetwork' | grep 'bridge'
docker network create --subnet=172.18.0.0/16 mynetwork
docker network ls

# 将数据存放到本地 -v $(pwd)/data:/data
# 本地配置 -v $(pwd)/redis.conf
# 不使用配置则使用默认配置：/usr/local/etc/redis/redis.conf
# 映射数据目录 rw 为读写
# 挂载配置文件 ro 为readonly
# --net bridge --ip 172.17.0.10  bridge：桥接网络  host： 主机网络
#     -d redis:5.0.6 \
docker run \
    --net mynetwork \
    --ip 172.18.0.2 \
    -p 6381:6379 \
    -v $(pwd)/data:/data:rw \
    -v $(pwd)/redis3.conf:/etc/redis/redis.conf \
    --restart=always \
    --privileged=true \
    --name redis-1 \
    -d redis:4.0.8 \
    redis-server /etc/redis/redis.conf --appendonly yes