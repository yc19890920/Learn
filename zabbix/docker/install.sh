#!/bin/sh

echo "启动一个空的Mysql服务器实例"
docker run --name mysql-server -t \
      -e MYSQL_DATABASE="zabbix" \
      -e MYSQL_USER="zabbix" \
      -e MYSQL_PASSWORD="zabbix" \
      -e MYSQL_ROOT_PASSWORD="zabbix" \
      -d mysql:5.7  \
      --character-set-server=utf8 --collation-server=utf8_bin


echo "启动Zabbix server实例，并关联这个实例到已创建的MySQL服务器实例"
docker run --name zabbix-server-mysql -t \
      -e DB_SERVER_HOST="mysql-server" \
      -e MYSQL_DATABASE="zabbix" \
      -e MYSQL_USER="zabbix" \
      -e MYSQL_PASSWORD="zabbix" \
      -e MYSQL_ROOT_PASSWORD="zabbix" \
      --link mysql-server:mysql \
      -p 10051:10051 \
      -d zabbix/zabbix-server-mysql:latest


echo "启动Zabbix web 接口，并将它与MySQL服务器实例和Zabbix server实例关联"
docker run --name zabbix-web-nginx-mysql -t \
      -e DB_SERVER_HOST="mysql-server" \
      -e MYSQL_DATABASE="zabbix" \
      -e MYSQL_USER="zabbix" \
      -e MYSQL_PASSWORD="zabbix" \
      -e MYSQL_ROOT_PASSWORD="zabbix" \
      --link mysql-server:mysql \
      --link zabbix-server-mysql:zabbix-server \
      -p 8002:80 \
      -d zabbix/zabbix-web-nginx-mysql:latest


echo "查看容器启动情况"
docker ps | grep zabbix


echo "访问web界面"
echo "http://192.168.1.24:8002"
echo "帐号密码: Admin / zabbix"




