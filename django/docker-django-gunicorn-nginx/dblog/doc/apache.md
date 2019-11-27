```
ERROR: Module mod-wsgi does not exist!
You will have to install mod wsgi as below. What you have to do is run the following commands,
sudo apt-get install libapache2-mod-wsgi
sudo a2enmod wsgi
```

## apache2 配置

1. 修改 静态目录 sudo chown ubuntu:www-data -R static/

2. 修改 /etc/apache2/ports.conf
```
添加一行
Listen 8080
```

3. 文件上传中文名乱码  vim /etc/apache2/envvars 

```
文件最后添加以下：
export LANG='zh_CN.UTF-8'
export LC_ALL='zh_CN.UTF-8'

nginx添加
vim /etc/nginx/nginx.conf 
http 中添加：
http { ...  charset  utf-8; .. }
```


4. 修改上传文件权限
- ps -ef | grep apache 查看apache 权限
- sudo chown -R www-data:www-data media/ 



5. 配置 /etc/apache2/conf-enabled/dblog.conf

```
WSGIPassAuthorization On
<VirtualHost *:8080>
ServerName djangoblog.com
ServerAlias www.djangoblog.com
WSGIProcessGroup djangoblog.com

WSGIDaemonProcess djangoblog.com python-path=/home/python/git/dblog:/home/python/pyenv/versions/django-blog/lib/python2.7/site-packages
WSGIScriptAlias / /home/python/git/dblog/dblog/wsgi.py
ErrorLog "/home/python/log/djangoblog_err"
CustomLog "/home/python/log/djangoblog" common

DocumentRoot "/home/python/git/dblog"

Alias /robots.txt /usr/local/yangcheng/dblog/static/robots.txt
# 存放用户上传图片等文件的位置，注意去掉#号
Alias /media/ /home/python/git/dblog/media/
# 静态文件(js/css/images)的存放位置
Alias /static/ /home/python/git/dblog/static/

<Directory /home/python/git/dblog/dblog>
        Require all granted
</Directory>

<Directory /home/python/git/dblog/dblog>
        <Files wsgi.py>
                #Allow from all
                Require all granted
        </Files>
</Directory>

#<Directory /home/python/git/dblog/static>
#        Order deny,allow
#        Allow from all
#</Directory>
#
#<Directory /home/python/git/dblog/media>
#        Order deny,allow
#        Allow from all
#</Directory>

</VirtualHost>
```
