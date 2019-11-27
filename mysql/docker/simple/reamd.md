介绍使用docker-compose 构建mysql 的基本配置

1.创建 docker-compose.yml文件
```
version: '3'
services:
    db:
        #构建mysql镜像
        image: mysql
        container_name: mysql-db # 容器名
        command: mysqld --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci #设置utf8字符集
        restart: always
        environment:
          MYSQL_ROOT_PASSWORD: root #root管理员用户密码
          MYSQL_USER: test   #创建test用户
          MYSQL_PASSWORD: test  #设置test用户的密码
        ports:
          - '6606:3306'  #host物理直接映射端口为6606
        volumes:
            #mysql数据库挂载到host物理机目录/e/docker/mysql/data/db
          - "/e/docker/mysql/data/db:/var/lib/mysql"  
            #容器的配置目录挂载到host物理机目录/e/docker/mysql/data/conf  
          - "/e/docker/mysql/data/conf:/etc/mysql/conf.d"
```

2.在 docker-compose.yml文件下的目录下，使用docker -compose命令 创建mysql数据库容器
docker-compose up -d


mysql -h127.0.0.1 -p6033 -uroot -p123456