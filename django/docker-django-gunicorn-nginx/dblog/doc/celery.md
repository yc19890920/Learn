## 异步队列任务
~/pyenv/versions/django-blog/bin/python manage.py  celery  worker  -c  4  --loglevel=info

## 定时任务队列
/home/ubuntu/pyenv/versions/django-blog/bin/celery  -A  dblog  beat  --loglevel=info 


## 启动celery 命令
用supervisor部署即可
执行目录： 
~/git/dblog

执行命令： 开启4个进程
~/pyenv/versions/django-blog/bin/celery  -A  dblog  worker -c  20  --loglevel=info
/home/ubuntu/pyenv/versions/django-blog/bin/celery  -A  dblog  worker -c  8  --loglevel=info

加上gevent 
~/pyenv/versions/django-blog/bin/celery  -A  dblog  worker -P gevent -c  20  --loglevel=info
/home/ubuntu/pyenv/versions/django-blog/bin/celery  -A  dblog  worker -P gevent -c  20  --loglevel=info


测试： 发表评论即可收到邮件了。

## supervisor配置
```
[program:celery]
command=/usr/bin/celery worker -A tasks
directory=/data/www
stdout_logfile=/data/logs/celery.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
# 在项目在虚拟环境下, 需要配置虚拟环境库所在的位置, 如下:environment=PYTHONPATH="$PYTHONPATH:/home/bosheng/work/vrxiio/lib/python2.7/site-packages"  

注释
;program:celery 要管理的进程名，你自己随便定义，我这定义了叫celery
;command  是启动celery的命令
;directory  是程序目录 ，因为我要启动celery，需要进入/data/www目录中才能生效的，所以这里在启动命令时，会切换到这个目录里
;autorstart  自动重启celery
;stdout_logfile  存放celery的日志路径

以上命令的大概意思就是：
进行到/data/www目录，然后执行/usr/bin/celery worker -A tasks，并把输出的日志保存到/data/logs/celery.log中，
这是指定了worker模式，如果不指定，默认为prefork模式，一般你机器有几核，系统就开启几个worker进程，如果有异常，记得查看日志/data/logs/celery.log
```