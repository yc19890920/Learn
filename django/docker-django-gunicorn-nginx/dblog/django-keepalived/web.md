1. 192.168.52.128 安装
apache2、nginx、redis、mysql  -- redis、mysql（暂不使用集群）

sudo apt install apache2
sudo vim /etc/apache2/ports.conf
修改 Listen 80 为 Listen 81

sudo apt install nginx
systemctl reload apache2.service nginx.service

sudo apt-get install redis-server
## 开启redis 允许外网IP 访问
vim /etc/redis/redis.conf 
bind 127.0.0.1 192.168.52.128
修改完成后，需要重新启动redis服务:  systemctl restart redis.service 
192.168.52.131 访问redis:    redis-cli -h 192.168.52.128 -p 6379

sudo apt-get install mysql
sudo apt install mysql-client
sudo mysql_secure_installation

sudo mysql -u root --skip-password  # 新版本安装过程中没有提示设置root用户密码
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';
mysql -h 127.0.0.1 -u dblog -P 3306 -p
mysql -h 192.168.52.128 -u dblog -P 3306 -p
- [Ubuntu18.04 安装 Mysql](https://yuan.ga/install-mysql-from-ubuntu18-04/)
systemctl restart mysql.service

sudo apt-get autoremove --purge mysql-server-5.7
sudo apt-get remove mysql-server
sudo apt-get autoremove mysql-server
sudo apt-get remove mysql-common //这个很重要
上面的其实有一些是多余的。
清理残留数据
dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P


CREATE DATABASE dblog DEFAULT CHARACTER SET UTF8;
create user 'dblog'@'%' identified by 'dblog123';
GRANT ALL ON dblog.* TO 'dblog'@'%';
flush  privileges;


# 开启服务端口
- [如何启动、关闭和设置ubuntu防火墙](https://blog.csdn.net/sdujava2011/article/details/51201061)
2.查看本地的端口开启情况(ubuntu下执行)： sudo ufw status
3.打开80端口(ubuntu下执行)：sudo ufw allow 8080
4.防火墙开启(ubuntu下执行)：sudo ufw enable
5.防火墙重启(ubuntu下执行)：sudo ufw reload
6. 禁用防火墙：sudo  ufw disable
7. 允许某特定 IP: sudo ufw allow from 192.168.254.254
8. 删除上面的规则: sudo ufw delete allow from 192.168.254.254

sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
sudo a2enmod wsgi
sudo service apache2 restart
systemctl reload apache2.service 
 
sudo apt-get install nginx
systemctl reload nginx.service


1. 192.168.52.128 安装
apache2、nginx、redis



## 两台机器apache配置
```
WSGIPassAuthorization On
<VirtualHost *:8080>
ServerName localhost
ServerAlias localhost
WSGIProcessGroup dblog

WSGIDaemonProcess dblog python-path=/home/python/dblog:/home/python/pyenv/versions/dblog/lib/python2.7/site-packages
WSGIScriptAlias / /home/python/dblog/dblog/wsgi.py
ErrorLog "/home/python/dblog/dblog_apache_error.log"
CustomLog "/home/python/dblog/dblog_apache.log" common

DocumentRoot "/home/python/dblog"

# 存放用户上传图片等文件的位置，注意去掉#号
Alias /media/ /home/python/dblog/media/
# 静态文件(js/css/images)的存放位置
Alias /static/ /home/python/dblog/static/

<Directory /home/python/dblog/dblog>
        Require all granted
</Directory>

<Directory /home/python/dblog/dblog>
        <Files wsgi.py>
                #Allow from all
                Require all granted
        </Files>
</Directory>

</VirtualHost>
```

## 两台机器nginx配置
```
# the upstream component nginx needs to connect to

upstream django80 {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8080; # for a web port socket (we'll use this first)
}


# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    server_name  192.168.52.131;

    access_log          /home/python/dblog/dblog_nginx.log;
    error_log           /home/python/dblog/dblog_nginx_erorr.log;

    proxy_connect_timeout    600;
    proxy_read_timeout       600;
    proxy_send_timeout       600;

    # max upload size
    client_max_body_size 50M;

    location ^~ /static/ {
        # your own static file
        root /home/python/dblog/;
        if ($query_string) {
            expires max;
        }
        expires 30d;
        break;
    }
        
   location /media/ {
        root /home/python/dblog/;
        expires 30d;
        break;
   }

    # Finally, send all non-media requests to the Django server.
   location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            #proxy_set_header Host $host;
            #proxy_set_header X-Real-IP $remote_addr;
            #proxy_set_header X-Server-Addr $server_addr;
            #proxy_set_header X-Remote-Addr $remote_addr;
            #proxy_set_header X-Remote-Port $remote_port;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://django80;
      }


        #-- Error page setting ---------------------------
        error_page          404              /404.html;
        error_page          500 502 503 504  /50x.html;
        location = /50x.html {
                 root            /home/python/dblog/templates/errpage;
        }
        location = /404.html {
                 root            /home/python/dblog/templates/errpage;
        }

}
```