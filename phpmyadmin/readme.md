- [Docker安装Mysql管理工具Phpmyadmin](https://xu3352.github.io/docker/2017/12/27/install-phpmyadmin-with-docker)
- [docker 部署 mysql + phpmyadmin 3种方法](https://blog.csdn.net/Gekkoou/article/details/80897309)

拉取镜像
# 搜索镜像
$ docker search phpmyadmin
NAME                     DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
phpmyadmin/phpmyadmin    A web interface for MySQL and MariaDB.          441                  [OK]
nazarpc/phpmyadmin       phpMyAdmin as Docker container, based on o...   56                   [OK]
......

# 没有官方的镜像, 那就默认打星最多的 (默认标签:latest)
$ docker pull phpmyadmin/phpmyadmin
初始化phpmyadmin容器
# 关联msyql容器初始化
$ docker run -d \
    --name myadmin \
    --link mysql:db \
    -p 8080:80 \
    phpmyadmin/phpmyadmin
详解:

-d - 以后台模式运行
--name myadmin - 容器命名为 myadmin, 容器管理时用(启动/停止/重启/查看日志等)
--link mysql:db - 容器关联, 这里我们关联到之前创建的 mysql 容器, 别名这里设置为 db
-p 8080:80 - 端口映射, 本地端口:容器端口, 访问: http://ip:8080
phpmyadmin/phpmyadmin - 要初始化的镜像名


关联独立的mysql服务器
# 比如阿里云的msyql服务器
$ docker run -d \
    --name myadmin_aliyun \
    -e PMA_HOST=xxx.mysql.rds.aliyuncs.com \
    -e PMA_PORT=3xx6 \
    -p 8081:80 \
    phpmyadmin/phpmyadmin
详解:

-e PMA_HOST=xxxx - 环境变量: mysql服务器域名或IP地址
-e PMA_PORT=3xx6 - 环境变量: mysql端口
如果不想每次都输入账号密码的话, 可以设置 PMA_USER 和 PMA_PASSWORD 环境变量(注意场合), 更多环境变量可以看此镜像的文档