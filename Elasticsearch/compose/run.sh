#!/usr/bin/env bash

DIR=$(pwd)

install(){
    mkdir -p ${DIR}/data/{es01,es02,es03}
    mkdir -p ${DIR}/logs/{es01,es02,es03}

    chmod -R 775 ${DIR}/data/{es01,es02,es03}  ${DIR}/logs/{es01,es02,es03}

    docker-compose up -d

    docker-compose ps
}


stop(){
    docker-compose stop es01 es02 es03
}

start(){
    docker-compose start es01 es02 es03
}

status(){
    docker-compose ps
}

remove(){
    #docker-compose stop es01 es02 es03

    echo "停止 elasticsearch 容器......"
    docker stop es01 es02 es03 kibana

    echo "删除 elasticsearch 容器......"
    docker rm es01 es02 es03 kibana

    echo "删除镜像......"
    # docker rmi redis/sentinel:1
    # docker rmi redis/sentinel:2

    echo 'y' | docker container prune
    echo 'y' | docker system prune

    rm -rf ${DIR}/logs/
    rm -rf ${DIR}/data/
}

case "$1" in
    "install"|"i")
        install;
        ;;
    "start")
        start;
        ;;
    "stop")
        stop;
        ;;
    "status")
        status;
        ;;
    "restart")
        stop;
        start;
        ;;
    "remove")
        remove;
        ;;
    *)
        echo "Usage: $basename {install|start|stop|status|restart|remove}" ;
        ;;
esac