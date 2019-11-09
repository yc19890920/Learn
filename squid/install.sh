#!/usr/bin/env bash

echo "安装 squid"
yum install squid

rpm -qa | grep squid

sed -i "s/211.159.69/61.144.165/g" `grep 211.159.69 -rl /etc/squid/squid.conf`