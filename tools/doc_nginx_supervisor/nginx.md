# nginx


### 卸载

``` bash
$ sudo apt-get remove --purge nginx nginx-core nginx-common
```

### 安装

``` bash
$ sudo apt-get install nginx
```

### 启动、停止、重启

``` bash
$ sudo /etc/init.d/nginx [start|stop|restart]
```

### 新建站点配置文件到 `/etc/nginx/sites-available/name`

``` bash
upstream app_server_django {
    server 127.0.0.1:8001 fail_timeout=0;
}

server {

    listen   80;
    server_name 127.0.0.1;
    charset    urf-8;

    client_max_body_size 4G;

    access_log /path/to/logs/nginx-access.log;
    error_log /path/to/logs/nginx-error.log;

    location /static/ {
        alias   /path/to/ProgramName/static/;
    }

    location /media/ {
        alias   /path/to/ProgramName/media/;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://app_server_django;
    }
}
```

创建符号链接

``` bash
$ sudo ln -s /etc/nginx/sites-available/ProgramName /etc/nginx/sites-enabled/ProgramName
```

### 重启

``` bash
$ sudo /etc/init.d/nginx restart
# OR
$ sudo service nginx restart
```

