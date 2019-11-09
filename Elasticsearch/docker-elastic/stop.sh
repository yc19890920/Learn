#!/usr/bin/env bash

echo "停止 elasticsearch 容器......"
docker stop es01 es02 es03 kibana

echo "删除 elasticsearch 容器......"
docker rm es01 es02 es03 kibana

echo "删除镜像......"
# docker rmi redis/sentinel:1
# docker rmi redis/sentinel:2


echo 'y' | docker container prune
echo 'y' | docker system prune
