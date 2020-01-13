#!/usr/bin/env bash

build(){
    cd /home/microk8s/code/Learn/Wizard
    echo "构建镜像"
    docker build -t my-wizard .
}

init(){
    echo "数据库初始化"
    docker run -it --rm --name my-wizard my-wizard php artisan migrate:install
    docker run -it --rm --name my-wizard my-wizard php artisan migrate
}

start(){
    cd /home/microk8s/code/Learn/Wizard
    docker run -d \
        --name my-wizard \
        -p 0.0.0.0:8080:80 \
        -v $(pwd)/wizard-file:/webroot/storage/app/public \
        my-wizard
}

bak_data(){
:<<EOF
    mysql数据库连接
    mysql -h 127.0.0.1 -u root -P 3306 -p
    123456

    创建数据库  wizard_2
    CREATE DATABASE wizard_2 DEFAULT CHARACTER SET UTF8;

    创建用户  wizard
    create user 'wizard'@'%' identified by 'wizard';

    授权 wizard 用户拥有 wizard_2 数据库的所有权限。
    GRANT ALL ON wizard_2.* TO 'wizard'@'%';

    启用修改
    flush  privileges;
EOF

    echo "备份数据"
    echo " mysqldump -u wizard -P 3306 -p wizard_2 > $(pwd)/my-wizard.sql"
    mysqldump -u wizard -P 3306 -p wizard_2 > $(pwd)/my-wizard.sql

}

reset_data(){
    echo "还原数据"
    echo " mysql -u root -p wizard_2 < $(pwd)/my-wizard.sql"
    mysql -u root -p wizard_2 < $(pwd)/my-wizard.sql
}

case "$1" in
    "start"|"s")
        build;
        # init;
        start;
        ;;
    "bak")
        bak_data;
        ;;
    "reset")
        reset_data;
        ;;
    *)
        echo "Usage: $0 {start|bak|reset}"
        ;;
esac

