#!/bin/bash

#for((i=1;i<1000;i++))
#do
#    # redis-cli -p 6382 set slave${i} ${i}
#    redis-cli -p 6382 DEL slave${i}
#    #sleep 5;
#done

for((i=1;i<1000;i++))
do
    # redis-cli -p 6382 set slave${i} ${i}
    redis-cli -p 6382 INCR master
    sleep 0.1;
done

