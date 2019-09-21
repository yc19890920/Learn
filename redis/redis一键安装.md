[root@redis-master ~]# cd /usr/local/src/
[root@redis-master src]# vim install_redis.sh
```
#!/usr/bin/env bash
# It's Used to be install redis.
# Created on 2018/04/08 11:18.
# @author: wangshibo.
# Version: 1.0
   
function install_redis () {
#################################################################################################
        cd /usr/local/src
        if [ ! -f " redis-4.0.1.tar.gz" ]; then
           wget http://download.redis.io/releases/redis-4.0.1.tar.gz
        fi
        cd /usr/local/src
        tar -zxvf /usr/local/src/redis-4.0.1.tar.gz
        cd redis-4.0.1
        make PREFIX=/usr/local/redis install
        mkdir -p /usr/local/redis/{etc,var}
        rsync -avz redis.conf  /usr/local/redis/etc/
        sed -i 's@pidfile.*@pidfile /var/run/redis-server.pid@' /usr/local/redis/etc/redis.conf
        sed -i "s@logfile.*@logfile /usr/local/redis/var/redis.log@" /usr/local/redis/etc/redis.conf
        sed -i "s@^dir.*@dir /usr/local/redis/var@" /usr/local/redis/etc/redis.conf
        sed -i 's/daemonize no/daemonize yes/g' /usr/local/redis/etc/redis.conf
        sed -i 's/^# bind 127.0.0.1/bind 0.0.0.0/g' /usr/local/redis/etc/redis.conf
 #################################################################################################
}
   
install_redis
```
[root@redis-master src]# chmod 755 install_redis.sh
[root@redis-master src]# sh -x install_redis.sh

