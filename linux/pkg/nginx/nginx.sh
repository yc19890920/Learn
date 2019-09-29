#!/bin/bash
### BEGIN INIT INFO
# Provides:       nginx
# Required-Start:    $local_fs $remote_fs $network $syslog $named
# Required-Stop:     $local_fs $remote_fs $network $syslog $named
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts the nginx web server
# Description:       starts nginx using start-stop-daemon
### END INIT INFO


PWDXXX=$(pwd)

TMP_CONF=${PWDXXX}/nginx2.conf

install_nginx(){
    cd ${PWDXXX}

    if [ -e ${PWDXXX}/test ]; then
        echo "nginx 已经安装"

        # 配置
        echo "<h1>Hello World</h1>" > ${PWDXXX}/test/html/index.html
        cp -rf $TMP_CONF  ${PWDXXX}/test/conf/nginx.conf
         echo "${PWDXXX}/test/sbin/nginx -c ${PWDXXX}/test/conf/nginx.conf"
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

        # 配置
        echo "<h1>Hello World</h1>" > ${PWDXXX}/test/html/index.html
        cp -rf $TMP_CONF  ${PWDXXX}/test/conf/nginx.conf
        # echo "${PWDXXX}/test/sbin/nginx -c ${PWDXXX}/test/conf/nginx.conf"
    fi
}
install_nginx;

#PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

#DAEMON=/usr/sbin/nginx
DAEMON=${PWDXXX}/test/sbin/nginx
NAME=nginx
DESC=nginx
NGINX_PID=${PWDXXX}/test/logs/nginx.pid
NGINX_CONF=${PWDXXX}/test/conf/nginx.conf

# Include nginx defaults if available
#if [ -r /etc/default/nginx ]; then
#        . /etc/default/nginx
#fi

# 从/etc/default/nginx引入的变量
#STOP_SCHEDULE="${STOP_SCHEDULE:-QUIT/5/TERM/5/KILL/5}"
STOP_SCHEDULE="QUIT/5/TERM/5/KILL/5"
ULIMIT="-n 4096"

test -x $DAEMON || exit 0

#. /lib/init/vars.sh
#. /lib/lsb/init-functions
. ${PWDXXX}/var.sh
. ${PWDXXX}/init-functions.sh


# Try to extract nginx pidfile
PID=$(cat $NGINX_CONF | grep -Ev '^\s*#' | awk 'BEGIN { RS="[;{}]" } { if ($1 == "pid") print $2 }' | head -n1)
if [ -z "$PID" ]; then
        PID=$NGINX_PID
fi

if [ -n "$ULIMIT" ]; then
        # Set ulimit if it is set in /etc/default/nginx
        ulimit $ULIMIT
fi

start_nginx() {
        # Start the daemon/service
        #
        # Returns:
        #   0 if daemon has been started
        #   1 if daemon was already running
        #   2 if daemon could not be started
        start-stop-daemon --start --quiet --pidfile $PID --exec $DAEMON --test > /dev/null \
                || return 1
        start-stop-daemon --start --quiet --pidfile $PID --exec $DAEMON -- \
                $DAEMON_OPTS 2>/dev/null \
                || return 2
}

test_config() {
        # Test the nginx configuration
        $DAEMON -t $DAEMON_OPTS >/dev/null 2>&1
}

stop_nginx() {
        # Stops the daemon/service
        #
        # Return
        #   0 if daemon has been stopped
        #   1 if daemon was already stopped
        #   2 if daemon could not be stopped
        #   other if a failure occurred
        start-stop-daemon --stop --quiet --retry=$STOP_SCHEDULE --pidfile $PID --name $NAME
        RETVAL="$?"
        sleep 1
        return "$RETVAL"
}

reload_nginx() {
        # Function that sends a SIGHUP to the daemon/service
        start-stop-daemon --stop --signal HUP --quiet --pidfile $PID --name $NAME
        return 0
}

rotate_logs() {
        # Rotate log files
        start-stop-daemon --stop --signal USR1 --quiet --pidfile $PID --name $NAME
        return 0
}

upgrade_nginx() {
        # Online upgrade nginx executable
        # http://nginx.org/en/docs/control.html
        #
        # Return
        #   0 if nginx has been successfully upgraded
        #   1 if nginx is not running
        #   2 if the pid files were not created on time
        #   3 if the old master could not be killed
        if start-stop-daemon --stop --signal USR2 --quiet --pidfile $PID --name $NAME; then
                # Wait for both old and new master to write their pid file
                while [ ! -s "${PID}.oldbin" ] || [ ! -s "${PID}" ]; do
                        cnt=`expr $cnt + 1`
                        if [ $cnt -gt 10 ]; then
                                return 2
                        fi
                        sleep 1
                done
                # Everything is ready, gracefully stop the old master
                if start-stop-daemon --stop --signal QUIT --quiet --pidfile "${PID}.oldbin" --name $NAME; then
                        return 0
                else
                        return 3
                fi
        else
                return 1
        fi
}

case "$1" in
        start)
                log_daemon_msg "Starting $DESC" "$NAME"
                start_nginx
                case "$?" in
                        0|1) log_end_msg 0 ;;
                        2)   log_end_msg 1 ;;
                esac
                ;;
        stop)
                log_daemon_msg "Stopping $DESC" "$NAME"
                stop_nginx
                case "$?" in
                        0|1) log_end_msg 0 ;;
                        2)   log_end_msg 1 ;;
                esac
                ;;
        restart)
                log_daemon_msg "Restarting $DESC" "$NAME"

                # Check configuration before stopping nginx
                if ! test_config; then
                        log_end_msg 1 # Configuration error
                        exit $?
                fi

                stop_nginx
                case "$?" in
                        0|1)
                                start_nginx
                                case "$?" in
                                        0) log_end_msg 0 ;;
                                        1) log_end_msg 1 ;; # Old process is still running
                                        *) log_end_msg 1 ;; # Failed to start
                                esac
                                ;;
                        *)
                                # Failed to stop
                                log_end_msg 1
                                ;;
                esac
                ;;
        reload|force-reload)
                log_daemon_msg "Reloading $DESC configuration" "$NAME"

                # Check configuration before stopping nginx
                #
                # This is not entirely correct since the on-disk nginx binary
                # may differ from the in-memory one, but that's not common.
                # We prefer to check the configuration and return an error
                # to the administrator.
                if ! test_config; then
                        log_end_msg 1 # Configuration error
                        exit $?
                fi

                reload_nginx
                log_end_msg $?
                ;;
        configtest|testconfig)
                log_daemon_msg "Testing $DESC configuration"
                test_config
                log_end_msg $?
                ;;
        status)
                status_of_proc -p $PID "$DAEMON" "$NAME" && exit 0 || exit $?
                ;;
        upgrade)
                log_daemon_msg "Upgrading binary" "$NAME"
                upgrade_nginx
                log_end_msg $?
                ;;
        rotate)
                log_daemon_msg "Re-opening $DESC log files" "$NAME"
                rotate_logs
                log_end_msg $?
                ;;
        *)
                echo "Usage: $NAME {start|stop|restart|reload|force-reload|status|configtest|rotate|upgrade}" >&2
                exit 3
                ;;
esac