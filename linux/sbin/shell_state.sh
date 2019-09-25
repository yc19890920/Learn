#!/bin/bash

# if 语句
#    if
#      判断命令，可以有很多个，真假取最后的返回值
#    then
#      如果前述为真做什么
#    [ # 方括号代表可选，别真打进去了！
#    elif
#      可以再来个判断，如果签名为假继续尝试这里
#    then
#      如果前述为真做什么 ]
#    else
#      如果全都不行做什么
#    fi # 结束，就是倒写的 if 啦。

#    -f "filename"
#    判断是否是一个文件
#    -x "/bin/ls"
#    判断/bin/ls是否存在并有可执行权限
#    -n "$var"
#    判断 $var 变量是否有值
#    "$a" == "$b"
#    判断$a和$b是否相等
#    -r "filename"
#    判断文件是否可读


# && 和 || 操作符
[ -f "/etc/shadow" ] && { echo "This computer uses shadow passwords"; }

#mailfolder="/var/spool/mail/james"
#[ -r "$mailfolder" ] || { echo "Can not read $mailfolder"; exit 1; }
#echo "$mailfolder has mail from:"
#grep "^From " $mailfolder


# case
case "$1" in
    "start")
        echo $1
        ;;
    "stop")
        echo $1
        ;;
    "status")
        echo $1
        ;;
    "restart")
        echo $1
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}" ;
        ;;
esac
#exit;

#    select 循环语句
#    select 循环语句是bash的一种扩展应用，擅长于交互式场合。
#    用户可以从一组不同的值中进行选择：
#    What is your favourite OS?
#    1) Linux
#    2) Gnu Hurd
#    3) Free BSD
#    4) Other
#    #? 1
#    You have selected Linux

#echo "What is your favourite OS?"
#select var in "Linux" "Gnu Hurd" "Free BSD" "Other"; do
#    break;
#done
#echo "You have selected $var"

# 3. for 循环

for var in A B C ; do
   echo "var is $var"
done

#普通循环
#for (( c=1; c<=5; c++ )); do
#   echo "Welcome $c times"
#done

#for (( i=1;i<5;i++ ))
#do
#    echo $i
#done

#4. while 循环
VAR=1
# 如果 VAR 小于 10，就打印出来
while [ $VAR -lt 10 ]
do
    echo $VAR
    #   VAR 自增 1
    VAR=`expr "$VAR" + 1`
done
