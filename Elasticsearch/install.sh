#!/bin/bash
:<<EOF

最后通过install命令来安装服务
sudo /usr/local/share/elasticsearch/bin/service/elasticsearch install

在这之后需要创建一个连接符号指向/usr/local/bin/elasticsearch下的/usr/local/share/elasticsearch/bin/service/elsaticsearch脚本，可以通过一下命令来实现
sudo ln -s 'readlink -f /usr/local/share/elasticsearch/bin/service/elasticsearch' /usr/local/bin/elasticsearch

这样以后想启动Elasticsearch，执行一下命令就可以了
/etc/init.d/elasticsearch start
EOF

HOME=$(pwd)
#PKG="elasticsearch-7.3.2-linux-x86_64.tar.gz"
PKG="elasticsearch-6.2.4.tar.gz"
ES_NAME="elasticsearch-6.2.4"
ES_BIN="/usr/local/bin/yc_elasticsearch"

JAVA_HOME=/usr/lib/jvm/java-12-oracle
JRE_HOME=${JAVA_HOME}/jre

install_java(){
    #    export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_144  ## 这里要注意目录要换成自己解压的jdk 目录
    #    export JRE_HOME=${JAVA_HOME}/jre
    #    export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
    #    export PATH=${JAVA_HOME}/bin:$PATH

#    wget https://download.java.net/java/GA/jdk11/28/GPL/openjdk-11+28_linux-x64_bin.tar.gz -O /tmp/openjdk-11+28_linux-x64_bin.tar.gz


    # 修改环境变量
    if [  `grep -c "${JAVA_HOME}" /root/.bashrc` -eq 0 ]; then
        cat >>/root/.bashrc<<EOF
export JAVA_HOME=/usr/lib/jvm/java-12-oracle
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
EOF
#        cat >>/root/.bashrc<<EOF
#export JAVA_HOME=/usr/lib/jvm/java-8-oracle
#export JRE_HOME=${JAVA_HOME}/jre
#export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
#export PATH=${JAVA_HOME}/bin:$PATH
#EOF
    else
        echo "java 已经存在环境变量中"
    fi

    # 系统注册此jdk
    # 现在我们已经有两个版本的 Java，我们可以通过 update-alternatives 来选择一个作为默认版本
    # update-alternatives –install /usr/bin/java java /usr/lib/jvm/java-8-oracle/bin/java 300
    java -version
    source /root/.bashrc
    return $?
}

install_es(){
    if [ ! -e ${HOME}/${PKG} ]; then
        wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.4.tar.gz
    fi

    if [ ! -e ${HOME}/${ES_NAME} ]; then
        tar -zxvf ${PKG}
        Ret=$?
        if [ $Ret -ne 0 ]; then
           echo "解压出错"
           exit 2
        else
           echo "解包完成"
        fi
    fi
    if [ -e ${ES_BIN} ]; then
        echo "yc_elasticsearch service exists"
    else
        echo ${HOME}/${ES_NAME}/bin/elasticsearch
        sudo ${HOME}/${ES_NAME}/bin/elasticsearch install
        ln -s ${HOME}/${ES_NAME}/bin/elasticsearch ${ES_BIN}
        # ${ES_BIN} start
    fi
}

start_es(){
    # ${ES_BIN} start
    ${HOME}/${ES_NAME}/bin/elasticsearch start
}

stop_es(){
    ${HOME}/${ES_NAME}/bin/elasticsearch stop
}

restart_es(){
    ${HOME}/${ES_NAME}/bin/elasticsearch restart
}

_RETURN=$? ;
case "$1" in
    "javaenv")
        install_java;
        _RETURN=$?;
        ;;
    "es")
        install_es;
        _RETURN=$?;
        ;;
    "start")
        start_es;
        _RETURN=$?;
        ;;
    "stop")
        stop_es;
        _RETURN=$?;
        ;;
    "restart")
        restart_es;
        _RETURN=$?;
        ;;
    *)
        echo "Usage: $0 {javaenv|es|start|stop|restart}"
        ;;
esac

exit $_RETURN











