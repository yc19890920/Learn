#!/bin/bash

CUR_PATH=$(pwd)
SQLPATH=$CUR_PATH/doc/sql
PYTHON_PATH="/home/python/pyenv/versions/edm_web/bin"
PYTHON="${PYTHON_PATH}/python"
PIP="${PYTHON_PATH}/pip"

# 数据库Server信息
HOSTNAME="127.0.0.1"
PORT="3306"
USERNAME="root"
#PASSWORD="123456"
# 要创建的数据库的库名称
# DBNAME=$1
DBNAME="spike"
DBNAME_USER="spike"
DBNAME_PASSWORD="123456"

function install_pkg() {
    $PIP install -r $CUR_PATH/doc/requirements.txt
    echo
    echo
}

function create_db_and_user() {
#    MYSQL_CMD="mysql -h${HOSTNAME}  -P${PORT}  -u${USERNAME} -p${PASSWORD}"
#    echo $MYSQL_CMD

#    CREATE DATABASE djblog DEFAULT CHARACTER SET UTF8;
#    create user 'djblog'@'%' identified by '123456';
#    GRANT ALL ON djblog.* TO 'djblog'@'%';
#    flush  privileges;

    MYSQL_CMD="mysql --defaults-extra-file=$SQLPATH/password1.txt"
    echo ${MYSQL_CMD}

    echo "创建数据库以及用户"
    # 创建数据库
    #echo "drop database ${DBNAME}"
    #create_db_sql="drop database IF EXISTS ${DBNAME}"
    #echo ${create_db_sql} | ${MYSQL_CMD}

    #判断是否创建成功

    echo "create database ${DBNAME}"
    create_db_sql="create database IF NOT EXISTS ${DBNAME} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
    echo "$create_db_sql"
    # 创建数据库
    echo "${create_db_sql}"  | ${MYSQL_CMD}
     #判断是否创建成功
    if [ $? -ne 0 ]; then
        echo "create databases ${DBNAME} failed ..."
        #exit 1
    fi

    echo "create user ${DBNAME}"
    # create_db_sql="grant all privileges on ${DBNAME}.* to ${DBNAME_USER}@'%' identified by '${DBNAME_PASSWORD}';"
    create_db_sql="create user '${DBNAME_USER}'@'%' identified by '123456'; GRANT ALL ON ${DBNAME}.* TO '${DBNAME_USER}'@'%'; flush  privileges;"
    echo "$create_db_sql"
    #exit 1;
     #创建数据库
    echo "${create_db_sql}"  | ${MYSQL_CMD}
     #判断是否创建成功
    if [ $? -ne 0 ]; then
        echo "create user ${DBNAME_USER} failed ..."
        #exit 1
    fi

    echo "flush  privileges;"  | ${MYSQL_CMD}
    echo
    echo
}


function sync_table() {
    cd ${CUR_PATH}/../web-django
    echo "检查数据表更新 makemigrations"
    $PYTHON manage.py makemigrations

    echo "运行Django命令行工具来自动创建数据库表 初始化表"
    $PYTHON manage.py migrate

    # 使用命令执行 sql 脚本文件
    echo "更新数据库表"
    echo "mysql --defaults-extra-file=$SQLPATH/password.txt < $SQLPATH/table.sql"
    mysql --defaults-extra-file=$SQLPATH/password.txt < $SQLPATH/table.sql

    echo "更新已有表的字段和索引"
    echo "mysql --defaults-extra-file=$SQLPATH/password.txt < $SQLPATH/update.sql"
    mysql --defaults-extra-file=$SQLPATH/password.txt < $SQLPATH/update.sql

    echo "$PYTHON ${CUR_PATH}/manage.py runserver 0.0.0.0:10086"

    echo
    echo
}

function import_data() {
    echo "导入数据（数据还原）"
    # mysql -u poetry -p poetry < ~/git/django2/db/djblog.sql
    echo "mysql  --defaults-extra-file=$SQLPATH/password.txt < ${CUR_PATH}/sql/backup.sql"
    mysql --defaults-extra-file=$SQLPATH/password.txt < ${CUR_PATH}/sql/backup.sql
}

function export_data() {
    echo "备份数据库"
    echo "mysqldump -u poetry -P 3306 -p poetry > ${CUR_PATH}/sql/backup.sql"
    #mysqldump  --defaults-extra-file=$SQLPATH/password.txt > ${CUR_PATH}/sql/backup.sql
    mysqldump -u poetry -P 3306 -p poetry > ${CUR_PATH}/sql/backup.sql
}

function django_run() {
    cd ${CUR_PATH}
    echo "${PYTHON_PATH}/gunicorn -c $CUR_PATH/doc/web-django.conf.py spike.wsgi:application"
    ${PYTHON_PATH}/gunicorn -c $CUR_PATH/doc/web-django.conf.py spike.wsgi:application
}

function flask_run() {
    cd ${CUR_PATH}
    echo "${PYTHON_PATH}/gunicorn -c web-flask.conf.py manage:app"
    ${PYTHON_PATH}/gunicorn -c web-flask.conf.py manage:app
}

function sanic_run() {
    cd ${CUR_PATH}
    echo "${PYTHON_PATH}/gunicorn -c web-sanic.conf.py manage:app"
    ${PYTHON_PATH}/gunicorn -c web-sanic.conf.py manage:app
}

#install_pkg;
#create_db_and_user;
#sync_table;
#import_data;

case "$1" in
    "init")
        install_pkg;
        create_db_and_user;
        sync_table;
        # import_data;
        ;;
    "backup")
        export_data;
        ;;
    "django")
        django_run;
        ;;
    "flask")
        flask_run;
        ;;
    "sanic")
        sanic_run;
        ;;
    *)
        echo "Usage: $0 {init|backup|django|sanic}"
        ;;
esac










