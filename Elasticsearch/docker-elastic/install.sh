#!/bin/bash


ELS="elasticsearch:6.7.0"
# ELS="elasticsearch:7.4.0"

echo "docker pull ${ELS}"
docker pull ${ELS}
#docker pull kibana:6.7.0

CUR_DIR=$(pwd)
DATA_CUR_DIR=$(pwd)
bind_host="0.0.0.0"
publish_host="192.168.1.24"
DOCKER_ES="/usr/share/elasticsearch"

# 注：设置-e ES_JAVA_OPTS="-Xms256m -Xmx256m" 是因为/etc/elasticsearch/jvm.options 默认jvm最大最小内存是2G，读者启动容器后 可用 docker stats 命令查看
# 1.在浏览器地址栏访问 http://192.168.1.24:9200/_cat/nodes?pretty 查看节点状态

mkdir -p ${CUR_DIR}/{config,data,logs}

PARAMS=('9201 9301 1'  '9202 9302 2'  '9203 9303 3')
for i in "${PARAMS[@]}" ; do
    # 此时b就相当于二维数组里面的一维数组了，然后可以再次遍历
    b=($i)
    echo "创建数据挂在卷：${CUR_DIR}/data/${b[0]}"
    mkdir -p ${DATA_CUR_DIR}/data/${b[0]}
    chmod 775 ${DATA_CUR_DIR}/data/${b[0]}
    mkdir -p ${DATA_CUR_DIR}/logs/${b[0]}
    chmod 775 ${DATA_CUR_DIR}/logs/${b[0]}

    echo "配置节点： tcp.port: ${b[0]}, tcp.port: ${b[1]}, node: es0${b[2]}"
    cat>${CUR_DIR}/config/${b[0]}.yml<<EOF
cluster.name: elasticsearch-cluster
node.name: es-node${b[2]}
network.bind_host: ${bind_host}
network.publish_host: ${publish_host}
http.port: ${b[0]}
transport.tcp.port: ${b[1]}
http.cors.enabled: true
http.cors.allow-origin: "*"
node.master: true
node.data: true
discovery.zen.ping.unicast.hosts: ["${publish_host}:9301","${publish_host}:9302","${publish_host}:9303"]
discovery.zen.minimum_master_nodes: 2
EOF

    echo "启动 elasticsearch"
    docker run -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \
    -d \
    -p ${b[0]}:${b[0]} \
    -p ${b[1]}:${b[1]} \
    -v ${CUR_DIR}/config/${b[0]}.yml:${DOCKER_ES}/config/elasticsearch.yml \
    -v ${DATA_CUR_DIR}/data/${b[0]}:${DOCKER_ES}/data \
    -v ${DATA_CUR_DIR}/logs/${b[0]}:${DOCKER_ES}/logs \
    --name es0${b[2]} \
    ${ELS}

done


docker ps -a | grep ${ELS}

# 启动 kibana
# 访问 http://yourip:5601

docker run \
    --link es01:elasticsearch \
    -p 5601:5601 \
    -v ${CUR_DIR}/config/kibana.yml:/usr/share/kibana/config/kibana.yml:ro \
    --name kibana \
    -d kibana:6.7.0

# 使用elasticsearch-head前端框架
# 浏览器访问http://192.168.1.24:9100/
# docker run -d -p 9100:9100 --name es-manager  mobz/elasticsearch-head
