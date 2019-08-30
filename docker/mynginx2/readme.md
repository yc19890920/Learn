## nginx 部署
首先，创建目录 nginx, 用于存放后面的相关东西。
`$ mkdir -p  nginx/www  nginx/logs  nginx/conf`

拷贝容器内 Nginx 默认配置文件到本地当前目录下的 conf 目录，容器 ID 可以查看 docker ps 命令输入中的第一列：

docker cp d1182cdce9b4:/etc/nginx/nginx.conf  nginx/conf/

- www: 目录将映射为 nginx 容器配置的虚拟目录。
- logs: 目录将映射为 nginx 容器的日志目录。
- conf: 目录里的配置文件将映射为 nginx 容器的配置文件。


## 部署命令
docker run -d -p 83:80 --name webnginx2 -v ~/Learn/docker/mynginx2/nginx/www:/usr/share/nginx/html -v ~/Learn/docker/mynginx2/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v ~/Learn/docker/mynginx2/nginx/logs:/var/log/nginx nginx

命令说明：
-p 8082:80： 将容器的 80 端口映射到主机的 83 端口。

--name webnginx2：将容器命名为 webnginx2。

-v ~/Learn/docker/mynginx2/nginx/www:/usr/share/nginx/html：将我们自己创建的 www 目录挂载到容器的 /usr/share/nginx/html。

-v ~/Learn/docker/mynginx2/nginx/conf/nginx.conf:/etc/nginx/nginx.conf：将我们自己创建的 nginx.conf 挂载到容器的 /etc/nginx/nginx.conf。

-v ~/Learn/docker/mynginx2/nginx/logs:/var/log/nginx：将我们自己创建的 logs 挂载到容器的 /var/log/nginx。


启动以上命令后进入 ~/nginx/www 目录：
cd nginx/www

创建 index.html 文件，内容如下：
```
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>菜鸟教程(runoob.com)</title>
</head>
<body>
    <h1>我的第一个标题</h1>
    <p>我的第一个段落。</p>
</body>
</html>
```






