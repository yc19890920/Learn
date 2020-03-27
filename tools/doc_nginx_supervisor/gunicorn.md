# Gunicorn（部署服务器）


### 安装

``` bash
$ pip install gunicorn
```

### 新建配置文件 `gunicorn_start.sh`

> 暂时放到项目根目录，考虑移到 `/bin` 下

``` bash
#!/bin/bash

ROOT=/path/to/ProgramName
APP=ProgramName.wsgi:application
NUM_WORKERS=2
HOST=127.0.0.1:8001
PID=/tmp/gunicorn.pid

cd $ROOT
source ../venv/bin/activate

exec gunicorn $APP --workers $NUM_WORKERS --bind $HOST --pid $PID
```

### 测试运行

``` bash
$ ./gunicorn_start.sh
```

> 运行时在 `/tmp` 下生成 gunicorn.pid 以便查看当前运行的 PID

