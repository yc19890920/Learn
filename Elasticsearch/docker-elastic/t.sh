#!/usr/bin/env bash

a=('9201 9301 1'  '9202 9302 2'  '9203 9303 3')

#for i in "${a[@]}" ; do
#    b=($i) #此时b就相当于二维数组里面的一维数组了，然后可以再次遍历
#    for j in "${b[@]}"; do
#        #do someting
#    done
#done

for i in "${a[@]}" ; do
    b=($i) #此时b就相当于二维数组里面的一维数组了，然后可以再次遍历
    echo ${b[0]}
    echo ${b[1]}
    echo ${b[2]}
done