# Supervisor（进程管理）


### 安装

``` bash
$ sudo pip install supervisor
```

### 生成配置文件

``` bash
$ echo_supervisord_conf > /etc/supervisord.conf
# 或
$ echo_supervisord_conf > /path/to/supervisord.conf
```

遇到权限问题时

``` bash
$ sudo su - root -c "echo_supervisord_conf > /etc/supervisord.conf"
```

### 在配置文件中添加要运行的项目

``` bash
[program:ProgramName]
command=/path/to/gunicorn_start.sh
directory=/path/to/ProgramName
startsecs=0
stopwaitsecs=0
autostart=true
autorestart=true
```

### 补充

生成的配置文件 supervisord.pid 以及 supervisor.sock 是放在 `/tmp` 目录下，但是 `/tmp` 目录是存放临时文件，里面的文件是会被 Linux 系统删除的，一旦这些文件丢失，就无法再通过 supervisorctl 来执行 restart 和 stop 命令了，将只会得到 unix:///tmp/supervisor.sock 不存在的错误。

``` bash
[unix_http_server]
;file=/tmp/supervisor.sock   ; (the path to the socket file)
file=/var/run/supervisor.sock ;修改为 /var/run 目录，避免被系统删除

[supervisord]
;logfile=/tmp/supervisord.log ; (main log file;default $CWD/supervisord.log)
logfile=/var/run/supervisord.log ;修改为 /var/run 目录，避免被系统删除
logfile_maxbytes=50MB        ; (max main logfile bytes b4 rotation;default 50MB)
logfile_backups=10           ; (num of main logfile rotation backups;default 10)
loglevel=info                ; (log level;default info; others: debug,warn,trace)
;pidfile=/tmp/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
pidfile=/var/run/supervisord.pid ;修改为 /var/run 目录，避免被系统删除
nodaemon=false               ; (start in foreground if true;default false)
minfds=1024                  ; (min. avail startup file descriptors;default 1024)
minprocs=200                 ; (min. avail process descriptors;default 200)
;设置启动 supervisord 的用户，一般情况下不要轻易用root用户来启动
;user=chrism                 ; (default is current user, required if root)

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

;必须和'unix_http_server'里面的设定匹配
[supervisorctl]
;serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket
serverurl=unix:///var/run/supervisor.sock ;修改为 /var/run 目录，避免被系统删除

[program:ProgramName]
command=/path/to/gunicorn_start.sh
directory=/path/to/ProgramName
startsecs=0
stopwaitsecs=0
autostart=true
autorestart=true
```

### 添加权限

``` bash
$ sudo chmod 777 /run
```

### 启动

``` bash
$ sudo supervisord
# OR
$ sudo supervisord -c /etc/supervisord.conf
```

### 启动、停止、重启管理的某个程序或所有程序

``` bash
$ sudo supervisorctl [start|stop|restart] [program-name|all]
```

### 查看状态

``` bash
$ sudo supervisorctl status
```

### 如果该配置文件没有放在 /etc/ 目录下，则需明确指定配置文件

``` bash
$ sudo supervisorctl -c /path/to/supervisord.conf [start|stop|restart] [program-name|all]
```

### 开机自动启动

``` bash
# 下载脚本
$ sudo su - root -c "sudo curl https://raw.githubusercontent.com/Supervisor/initscripts/master/ubuntu > /etc/init.d/supervisord"
```
注意：这个脚本下载下来后，还需检查一下与我们的配置是否相符合，比如默认的配置文件路径，pid 文件路径等，如果存在不同则需要进行一些修改。

pip 安装的应该在 `/usr/local/bin` 目录下

``` bash
DAEMON=/usr/local/bin/supervisord
SUPERVISORCTL=/usr/local/bin/supervisorctl

DAEMON_OPTS="-c /etc/supervisord.conf $DAEMON_OPTS"
```

``` bash
# 创建文件夹
$ sudo mkdir -p /var/run/supervisor
$ sudo mkdir -p /var/log/supervisor
```

``` bash
# 设置该脚本为可以执行
$ sudo chmod +x /etc/init.d/supervisord

# 设置为开机自动运行
$ sudo update-rc.d supervisord defaults

# 运行
$ sudo /etc/init.d/supervisord [start|stop|restart]
```

[:link:](http://www.restran.net/2015/10/04/supervisord-tutorial/)
[:link:](http://www.codeif.com/post/ubuntu-install-supervisor/)

