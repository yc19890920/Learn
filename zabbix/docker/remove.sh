#!/usr/bin/env bash


docker stop  mysql-server zabbix-server-mysql zabbix-web-nginx-mysql

echo 'y' | docker system prune
