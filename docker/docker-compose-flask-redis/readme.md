使用docker build -t composeapp . 指令创建composeapp镜像。
$ docker build -t composeapp .
$ docker images


4.可以使用-d选项，以守护方式运行compose
$ docker-compose up -d
$ docker-compose -f docker-compose.yml -p flask-app-redis up -d 

5.查看日志信息
$ docker-compose ps
$ docker-compose logs flask-app
$ docker-compose logs flask-redis

6.使用docker-compose port web 5000 查看web服务5000端口映射情况
$ docker-compose port flask-app 5000
0.0.0.0:5000

注意：操作docker-compose命令要跟docker-compose.yml在同一目录，否则无法操作。

7.网页访问web计数器
刷新浏览器，times会依次递增