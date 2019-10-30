#!/usr/bin/env bash

echo "停止redis容器......"
docker stop redis-master redis-slave \
    compose_redis-slave_1 compose_redis-slave_2 \
    compose_redis-sentinel_1 compose_redis-sentinel_2 compose_redis-sentinel_3

echo "删除redis容器......"
docker rm redis-master redis-slave \
    compose_redis-slave_1 compose_redis-slave_2 \
    compose_redis-sentinel_1 compose_redis-sentinel_2 compose_redis-sentinel_3

echo "删除镜像......"
# docker rmi redis/sentinel:1
# docker rmi redis/sentinel:2


echo 'y' | docker container prune
echo 'y' | docker system prune
