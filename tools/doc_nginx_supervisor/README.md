# 部署（Ubuntu）


### 1、下载代码

### 2、修改 settings.py

填写邮箱服务器帐号密码

``` python
# settings.py

DEBUG: False

ALLOWED_HOSTS = ['*',]
```


### 3、虚拟环境

``` bash
$ virtualenv venv --python=python3.4
$ source venv/bin/activate
(venv) $ pip install -U pip
(venv) $ pip install -r requirements.txt

# DEBUG 为 False 需同步后台静态文件
(venv)$ python manage.py collectstatic
```

### 4、生成表

``` bash
(venv) $ python manage.py makemigrations
(venv) $ python manage.py migrate
(venv) $ python manage.py createsuperuser
```

### 5、[gunicorn](gunicorn.md)

### 6、[supervisor](supervisor.md)

### 7、[nginx](nginx.md)

