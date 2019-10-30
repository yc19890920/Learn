#!/usr/bin/env bash

CUR=$(pwd)
wget http://download.redis.io/releases/redis-5.0.6.tar.gz

tar xvzf redis-5.0.6.tar.gz

cd ${CUR}/redis-5.0.6/deps

make hiredis jemalloc linenoise lua

cd ${CUR}/redis-5.0.6

make && make install

cp /usr/local/bin/redis-* /usr/bin/

# 后台启动
redis-server &






