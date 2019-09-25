#!/bin/bash

PYENV="/home/python/pyenv"
VIRTUAENV="/home/python/pyenv/plugins/pyenv-virtualenv"
PYTHON37="/home/python/pyenv/versions/3.7.0/bin/python"
PYTHON_HAYSTACK="/home/python/pyenv/versions/haystack/bin/python"
PYTHON_HAYSTACK_PIP="/home/python/pyenv/versions/haystack/bin/pip"

PROJECT="/home/python/Learn/django/Haystack-Whoosh/haystackwhoosh"
PROJECT_DIR="/home/python/Learn/django/Haystack-Whoosh"
DJANGO_ADMIN="/home/python/pyenv/versions/haystack/bin/django-admin"

update_apt(){
    sudo apt-get install libc6-dev gcc
    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm

    git clone https://github.com/yyuu/pyenv.git  /home/python/pyenv
    echo 'export PATH=/home/python/pyenv/bin:$PATH' >> ~/.bashrc
    echo 'export PYENV_ROOT=/home/python/pyenv' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    source ~/.bashrc
}

# 安装python3.7.0
install_python(){
    pyenv install 3.7.0 -v
    pyenv rehash
    pyenv versions
}

install_pkg(){
    # 安装pyenv
    if [ -e $PYENV ]; then
        echo "pyenv exists"
    else
        update_apt;
        install_python;
    fi

    # 安装 pyenv-virtualenv
    if [ -e $PYENV ]; then
        echo "pyenv-virtualenv exists"
    else
        git clone https://github.com/yyuu/pyenv-virtualenv.git  /home/python/pyenv/plugins/pyenv-virtualenv
        echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
        source .bashrc
    fi

    # 安装python3.7.0
    if [ -e $PYTHON37 ]; then
        echo "python 3.7 exists"
    else
        install_python;
    fi

    # 安装 python 全文搜索运行环境
    if [ -e $PYTHON_HAYSTACK ]; then
        echo "python 3.7 全文搜索运行环境已安装"
    else
        pyenv virtualenv 3.7.0 haystack
    fi
}


create_project(){

    if [ -e $PROJECT_DIR/requirements.txt -a -s $PROJECT_DIR/requirements.txt ]; then
        rm $PROJECT_DIR/requirements.txt
        $PYTHON_HAYSTACK_PIP install django whoosh django-haystack jieba hiredis redis meinheld gunicorn pymysql
        echo "requrements exists"
    else
        $PYTHON_HAYSTACK_PIP install django whoosh django-haystack jieba hiredis redis meinheld gunicorn pymysql
    fi

    $PYTHON_HAYSTACK_PIP freeze > $PROJECT_DIR/requirements.txt

    cd $PROJECT_DIR

    if [ -e $PROJECT/manage.py ]; then
        echo "haystack-whoosh exists"
    else
        $DJANGO_ADMIN startproject haystackwhoosh
    fi

    if [ -d $PROJECT/app ]; then
        echo
    else
        mkdir -p $PROJECT/app
        touch $PROJECT/app/__init__.py
     fi

    cd $PROJECT/app
    if [ -d $PROJECT/app/core ]; then
        echo "core app exists"
    else
        $PYTHON_HAYSTACK $PROJECT/manage.py startapp core
    fi

    if [ -e $PROJECT/app/blog ]; then
        echo "blog app exists"
    else
        $PYTHON_HAYSTACK $PROJECT/manage.py startapp blog
    fi

    echo "创建项目成功"
}

start_project(){
    # 检查数据表更新
    echo -e "检查数据表更新：\n $PYTHON_HAYSTACK $PROJECT/manage.py makemigrations"
    $PYTHON_HAYSTACK $PROJECT/manage.py makemigrations

    # 运行Django命令行工具来自动创建数据库表 初始化表
    echo -e "初始化表：\n $PYTHON_HAYSTACK $PROJECT/manage.py migrate"
    $PYTHON_HAYSTACK $PROJECT/manage.py migrate

    # 创建用户
    if [ -e $PROJECT/user.txt ]; then
        echo "user exists"
    else
        echo "create superuser: user: admin / password: 1qaz@WSX / email: test@test.com"
        $PYTHON_HAYSTACK $PROJECT/manage.py createsuperuser
        echo "admin / 1qaz@WSX" >> $PROJECT/user.txt
    fi

    if [ -e $PROJECT/sync.txt ]; then
        echo "sync exists"
    else
        $PYTHON_HAYSTACK $PROJECT/sync_data.py
        echo "1" >> $PROJECT/sync.txt
    fi

    # 构建whoosh 全文索引
    echo -e "构建whoosh 全文索引：\n $PYTHON_HAYSTACK $PROJECT/manage.py rebuild_index"
    $PYTHON_HAYSTACK $PROJECT/manage.py rebuild_index   # or update_index

    echo -e "运行：\n $PYTHON_HAYSTACK  $PROJECT/manage.py runserver 0.0.0.0:9999"
    $PYTHON_HAYSTACK  $PROJECT/manage.py runserver 0.0.0.0:9999
}

install_pkg;
create_project;
start_project;
exit $?;

