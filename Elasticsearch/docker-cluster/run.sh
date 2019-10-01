#!/bin/bash

docker pull elasticsearch:6.7.0
docker pull kibana:6.7.0

mkdir -p mnt/data1
mkdir -p mnt/data2
mkdir -p mnt/data3
chmod 777 $(pwd)/mnt/data1
chmod 777 $(pwd)/mnt/data2
chmod 777 $(pwd)/mnt/data3

DOCKER_ES="/usr/share/elasticsearch"

# 注：设置-e ES_JAVA_OPTS="-Xms256m -Xmx256m" 是因为/etc/elasticsearch/jvm.options 默认jvm最大最小内存是2G，读者启动容器后 可用 docker stats 命令查看
# 1.在浏览器地址栏访问 http://192.168.1.24:9200/_cat/nodes?pretty 查看节点状态
docker run -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \
    -d \
    -p 9200:9200 \
    -p 9300:9300 \
    -v $(pwd)/mnt/config/es1.yml:${DOCKER_ES}/config/elasticsearch.yml \
    -v $(pwd)/mnt/data1:${DOCKER_ES}/data \
    --name es01 \
    elasticsearch:6.7.0

docker run -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \
    -d \
    -p 9201:9201 \
    -p 9301:9301 \
    -v $(pwd)/mnt/config/es2.yml:${DOCKER_ES}/config/elasticsearch.yml \
    -v $(pwd)/mnt/data2:${DOCKER_ES}/data \
    --name es02 \
    elasticsearch:6.7.0

docker run -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \
    -d \
    -p 9202:9202 \
    -p 9302:9302 \
    -v $(pwd)/mnt/config/es3.yml:${DOCKER_ES}/config/elasticsearch.yml \
    -v $(pwd)/mnt/data3:${DOCKER_ES}/data \
    --name es03 \
    elasticsearch:6.7.0

# 启动 kibana
# 访问 http://yourip:5601
docker run \
    --link es01:elasticsearch \
    -p 5601:5601 \
    -v $(pwd)/mnt/kibana.yml:/usr/share/kibana/config/kibana.yml:ro \
    --name kibana \
    -d kibana:6.7.0

# 使用elasticsearch-head前端框架
# 浏览器访问http://192.168.1.24:9100/
# docker run -d -p 9100:9100 --name es-manager  mobz/elasticsearch-head
