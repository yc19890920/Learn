#!/bin/bash

:<<EOF
web 调试启动快捷键设置

 chmod 777 webrun.sh
 sudo cp web_debug.sh /etc/init.d/yc-webrun
 /etc/init.d/webrun webvue

 设置当前用户系统命令
  vim /home/python/.bashrc
  source /home/python/.bashrc
  alias ycvue="/etc/init.d/yc-webrun webvue"
  alias ycoperation="/etc/init.d/yc-webrun operation"
  alias ycedm="/etc/init.d/yc-webrun edmweb"
  alias yczhimeng="/etc/init.d/yc-webrun zhimeng"
  alias ycgit="/etc/init.d/yc-webrun pycgitdel"
  alias yclearn="/etc/init.d/yc-webrun pyclearndel"

 source ~/.bashrc

 解决.bashrc文件每次打开终端都需要source的问题
这个问题困扰我很久，我明明改了~/.bashrc文件，重新通过ssh登录的时候每次我都要手动输入source ~/.bashrc，配置才会生效，很是头疼，于是我就研究了一下解决办法以及问题的原因是什么。
    解决方法
    vim ~/.bash_profile 在文件内部输入
    # 加载.bashrc文件
    if test -f .bashrc ; then
        source .bashrc
    fi
    在.bash_profile文件中自动加载.bashrc文件。
EOF

start_webvue(){
    CMD="/home/python/pyenv/versions/Linux-Opration/bin/python /home/python/Linux-WebVue/manage.py runserver 0.0.0.0:9990"
    # tr 将命令压缩各个列之间的空格，将多个空格压缩为一个，接着使用cut命令根据空格对列进行分割并取出第二个位置的值，也就是PID
    PID=$(ps aux | grep "$CMD" | grep -v 'grep' | tr -s ' '| cut -d ' ' -f 2)
    echo
    if [ ! -n $PID ]; then
        echo "service is running, then kill $PID"
        kill $PID
    fi
    exec $CMD
    return $?
}

start(){
    # 应该为 $@ 而不是 $1
    CMD=$@
    echo "CMD： $@"
    # tr 将命令压缩各个列之间的空格，将多个空格压缩为一个，接着使用cut命令根据空格对列进行分割并取出第二个位置的值，也就是PID
    PID=$(ps aux | grep "$CMD" | grep -v 'grep' | tr -s ' '| cut -d ' ' -f 2)
    if [ ! -n "$PID" ]; then
        echo "service is not running"
    else
        echo "service is running, then kill $PID"
        kill $PID
    fi
    exec $CMD
    return $?
}

delete_lern_pyc(){
    cd /home/python/Learn
    find . -name "*.pyc"  | xargs -n 10 rm -f
}

delete_git_pyc(){
    cd /home/python/git
    find . -name "*.pyc"  | xargs -n 10 rm -f
}

_RETURN=$? ;
case "$1" in
    "webvue")
        CMD='/home/python/pyenv/versions/Linux-Opration/bin/python /home/python/Linux-WebVue/manage.py runserver 0.0.0.0:9990'
        start $CMD;
        _RETURN=$?;
        ;;
    "operation")
        CMD="/home/python/pyenv/versions/Linux-Opration/bin/python /home/python/Linux-Operation/manage.py runserver 0.0.0.0:10001"
        start $CMD;
        _RETURN=$?;
        ;;
    "edmweb")
        CMD="/home/python/pyenv/versions/edm_web/bin/python /home/python/edm_web/manage.py runserver 0.0.0.0:8069"
        start $CMD;
        _RETURN=$?;
        ;;
    "zhimeng")
        CMD="/home/python/pyenv/versions/edm_web/bin/python /home/python/zhi_meng/manage.py runserver 0.0.0.0:7070"
        start $CMD;
        _RETURN=$?;
        ;;
    "zhimeng")
        CMD="/home/python/pyenv/versions/edm_web/bin/python /home/python/zhi_meng/manage.py runserver 0.0.0.0:7070"
        start $CMD;
        _RETURN=$?;
        ;;
    "pycgitdel")
        delete_git_pyc;
        ;;
    "pyclearndel")
        delete_lern_pyc;
        ;;
    *)
        echo "Usage: $0 {webvue|operation|edmweb|zhimeng}"
        ;;
esac

exit $_RETURN
