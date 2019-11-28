#!/usr/bin/env bash

function install() {
    docker run -d \
        --name phphmyadmin_local \
        -e PMA_HOST=192.168.1.24 \
        -e PMA_PORT=3306 \
        -p 8081:80 \
        phpmyadmin/phpmyadmin

    sleep 10
    status;
}

function stop() {
    docker stop phphmyadmin_local
    echo "y" | docker system prune
}

function status(){
    docker ps -a | grep phphmyadmin_local
}



case "$1" in
    "install"|"i")
        install
        ;;
    "stop")
        stop
        ;;
    "status")
        status
        ;;
    *)
        echo "Usage: $basename {install|stop|status}" ;
        _RET_VAL=1
        ;;
esac