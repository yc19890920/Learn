#!/usr/bin/env bash

#我们经常需要在 Shell 脚本中计算，掌握基本的运算方法很有必要，下面就是 4 种比较常见的运算方法，功能都是将 m + 1：
#1. m=$[ m + 1 ]
#2. m=expr $m + 1 # 用 “ 字符包起来
#3. let m=m+1
#4. m=$(( m + 1 ))

var=1
var=$var+1
echo $var # 输出 1+1

unset var
var=1
var=`expr "$var" + 1`
echo $var

#let var=var+1
var=$(( var + 1 ))
echo $var


a=10
b=20

val=`expr $a + $b`
echo "a + b : $val"

val=`expr $a - $b`
echo "a - b : $val"

val=`expr $a \* $b`
echo "a * b : $val"

val=`expr $b / $a`
echo "b / a : $val"

val=`expr $b % $a`
echo "b % a : $val"

if [ $a == $b ]; then
   echo "a 等于 b"
else
    echo "a 不等于 b"
fi

#if [ $a != $b ]; then
#   echo "a 不等于 b"
#fi

if [ $a -eq $b ]
then
   echo "$a -eq $b : a 等于 b"
else
   echo "$a -eq $b: a 不等于 b"
fi
if [ $a -ne $b ]
then
   echo "$a -ne $b: a 不等于 b"
else
   echo "$a -ne $b : a 等于 b"
fi
if [ $a -gt $b ]
then
   echo "$a -gt $b: a 大于 b"
else
   echo "$a -gt $b: a 不大于 b"
fi
if [ $a -lt $b ]
then
   echo "$a -lt $b: a 小于 b"
else
   echo "$a -lt $b: a 不小于 b"
fi
if [ $a -ge $b ]
then
   echo "$a -ge $b: a 大于或等于 b"
else
   echo "$a -ge $b: a 小于 b"
fi
if [ $a -le $b ]
then
   echo "$a -le $b: a 小于或等于 b"
else
   echo "$a -le $b: a 大于 b"
fi