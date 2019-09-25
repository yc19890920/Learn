#!/bin/bash

num1=100
num2=200

if test $num1 -eq $num2; then
    echo "相等"
else
    echo "不相等"
fi

a=5
b=6

result=$[ a + b ] # 注意等号两边不能有空格
echo "result 为： $result"

a=0
until [ ! $a -lt 10 ]
do
   echo $a
   a=`expr $a + 1`
done

while :
do
    echo -n "输入 1 到 5 之间的数字:"
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的! 游戏结束"
            break
        ;;
    esac
done

for((i=1;i<=5;i++));do
    echo "这是第 $i 次调用";
done;