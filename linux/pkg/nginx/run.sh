#!/bin/bash

PWDXXX=$(pwd)

install_nginx(){
    cd ${PWDXXX}

    if [ -e ${PWDXXX}/test ]; then
        echo "nginx 已经安装"
    else
        # 安装依赖
        sudo apt-get install gcc zlib1g-dev libpcre3 libpcre3-dev libssl-dev

        # 下载nginx
        NGINX_VERSION="1.9.9"
        if [! -e ${PWDXXX}/nginx-${NGINX_VERSION}.tar.gz ]; then
            wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz
        else
            echo "nginx-${NGINX_VERSION}.tar.gz 已经存在"
        fi

        # 解压并进入目录
        tar -xvf nginx-${NGINX_VERSION}.tar.gz
        mv nginx-${NGINX_VERSION} nginx
        cd ${PWDXXX}/nginx

        # 编译和安装
        #    ./configure --prefix=/usr/local/test
        #    可以把所有资源文件放在/usr/local/test的路径中，不会杂乱。
        #    用了—prefix选项的另一个好处是卸载软件或移植软件。当某个安装的软件不再需要时，只须简单的删除该安装目录，就可以把软件卸载得干干净净；移植软件只需拷贝整个目录到另外一个机器即可（相同的操作系统）。
        #    当然要卸载程序，也可以在原来的make目录下用一次make uninstall，但前提是make文件指定过uninstall。
        mkdir -p ${PWDXXX}/test
        echo "prefix: ${PWDXXX}/test"
        sleep 5;
        ./configure --prefix=${PWDXXX}/test
        make && make install
    fi
}

start_nginx(){
    echo "<h1>Hello World</h1>" > ${PWDXXX}/test/html/index.html
    cp -rf ${PWDXXX}/nginx.conf  ${PWDXXX}/test/conf/nginx.conf
    echo "${PWDXXX}/test/sbin/nginx -c ${PWDXXX}/test/conf/nginx.conf"

#    PID=$(ps aux | grep "${PWDXXX}/test/sbin/nginx -c ${PWDXXX}/test/conf/nginx.conf" | grep -v 'grep' | tr -s ' '| cut -d ' ' -f 2)
#    if [ -n $PID ]; then
#        exec ${PWDXXX}/test/sbin/nginx -c ${PWDXXX}/test/conf/nginx.conf
#    fi
}

. ${PWDXXX}/var.sh
. ${PWDXXX}/init-functions.sh

###################################
# Start nginx daemons functions.
nginx_pid="${PWDXXX}/test/logs/nginx.pid"
nginxd="${PWDXXX}/test/sbin/nginx"
nginx_config="${PWDXXX}/test/conf/nginx.conf"
lock_nginx="${PWDXXX}/test/logs/lock-nginx"
NAME=nginx

# Try to extract nginx pidfile
PID=$(cat $nginx_config | grep -Ev '^\s*#' | awk 'BEGIN { RS="[;{}]" } { if ($1 == "pid") print $2 }' | head -n1)
if [ -z "$PID" ]; then
        PID=$nginx_pid
fi

start() {
    if [ -e $PID ];then
        if ps aux|grep -v grep |grep "nginx"|awk '{print $2}'|grep "$pid" >/dev/null ; then
            echo "$NAME already running...."
                exit 1
            else
                rm -f $PID;
            fi
    fi

    echo -n $"Starting $NAME: "
    daemon $nginxd -c ${nginx_config}
    RETVAL=$?
    echo
    #    [ $RETVAL = 0 ] && touch /var/lock/subsys/nginx
    [ $RETVAL = 0 ] && touch $lock_nginx
    return $RETVAL

}


# Stop nginx daemons functions.
stop() {
        echo -n $"Stopping $NAME: "
        killproc $nginxd
        RETVAL=$?
        echo
        # [ $RETVAL = 0 ] && rm -f /var/lock/subsys/nginx /usr/local/u-mail/service/nginx/logs/nginx.pid
        [ $RETVAL = 0 ] && rm -f $lock_nginx $PID
}


# reload nginx service functions.
reload() {
    echo -n $"Reloading $NAME: "
    # kill -HUP `cat ${PID}`
    killproc $nginxd -HUP
    RETVAL=$?
    echo
}

install_nginx;
start_nginx;

# See how we were called.
case "$1" in
    start)
            start
            ;;

    stop)
            stop
            ;;

    reload)
            reload
            ;;

    restart)
            stop
            start
            ;;

    status)
            status $NAME
            RETVAL=$?
            ;;
    *)
            echo $"Usage: $NAME {start|stop|restart|reload|status|help}"
            exit 1
esac

exit $RETVAL




