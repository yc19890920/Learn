#! /bin/bash

# 创建容器时，最后mysql:5.7表示mysql镜像的版本，可以写，表示指定该版本；
# 如果不写也可以，docker会自动在本地检测有没有最新的，如果没有会自动去docker hub上去下载。
docker run -p 6034:3306 \
    --name qmm-mysql \
    -v $(pwd)/data2/db:/var/lib/mysql \
    -v $(pwd)/data2/conf:/etc/mysql/conf.d \
    -e MYSQL_ROOT_PASSWORD=123456  \
    -e MYSQL_USER=test \
    -e MYSQL_PASSWORD=test \
    -d mysql:5.7
