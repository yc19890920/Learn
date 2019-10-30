#!/usr/bin/env bash

echo "停止redis容器......"
docker stop Redis-master Redis-slave-1 Redis-slave-2 Redis-slave-3 Redis-sentinel-1 Redis-sentinel-2 Redis-sentinel-3 Redis-sentinel-4

echo "删除redis容器......"
docker rm Redis-master Redis-slave-2 Redis-slave-1 Redis-slave-3 Redis-sentinel-1 Redis-sentinel-2 Redis-sentinel-3 Redis-sentinel-4

echo "删除镜像......"
docker rmi redis/sentinel:1
docker rmi redis/sentinel:2


echo 'y' | docker container prune
echo 'y' | docker system prune
