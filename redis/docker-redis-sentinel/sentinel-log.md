哨兵的输出：

//+sdown：master节点挂了。后面是master信息
# +sdown master mymaster 192.168.2.100 6379    

# +odown master mymaster 192.168.2.100 6379 #quorum 1/1

# +new-epoch 14

//开始恢复故障
# +try-failover master mymaster 192.168.2.100 6379    

//投票选举节点的哨兵信息，因为我们就一个哨兵，所以就是自己 leader
# +vote-for-leader e49df1197325687d9a40508c00f466a8c6e596db 14   

//选举节点后替换谁
# +elected-leader master mymaster 192.168.2.100 6379  

//开始为故障的master选举
# +failover-state-select-slave master mymaster 192.168.2.100 6379

                    
//节点选举结果，选中192.168.2.200:6379来替换master
# +selected-slave slave 192.168.2.200:6379 192.168.2.200 6379 @ mymaster 192.168.2.100 6379


//确认节点选举结果
* +failover-state-send-slaveof-noone slave 192.168.2.200:6379 192.168.2.200 6379 @ mymaster 192.168.2.100 6379

                   
//选中的节点正在升级为master
* +failover-state-wait-promotion slave 192.168.2.200:6379 192.168.2.200 6379 @ mymaster 192.168.2.100 6379

                    
//选中的节点已成功升级为master
# +promoted-slave slave 192.168.2.200:6379 192.168.2.200 6379 @ mymaster 192.168.2.100 6379

                    
 //切换故障master的状态
# +failover-state-reconf-slaves master mymaster 192.168.2.100 6379

                   

* +slave-reconf-sent slave 192.168.2.201:6379 192.168.2.201 6379 @ mymaster 192.168.2.100 6379


//其他节点同步故障master信息
* +slave-reconf-inprog slave 192.168.2.201:6379 192.168.2.201 6379 @ mymaster 192.168.2.100 6379

                   
//其他节点完成故障master的同步
* +slave-reconf-done slave 192.168.2.201:6379 192.168.2.201 6379 @ mymaster 192.168.2.100 6379

                    
//故障恢复完成
# +failover-end master mymaster 192.168.2.100 6379

                    
//master从192.168.2.100:6379  变为 192.168.2.200:6379
# +switch-master mymaster 192.168.2.100 6379 192.168.2.200 6379

                    
//其他节点指定新的master
* +slave slave 192.168.2.201:6379 192.168.2.201 6379 @ mymaster 192.168.2.200 6379

                    
//故障master指定新的master
* +slave slave 192.168.2.100:6379 192.168.2.100 6379 @ mymaster 192.168.2.200 6379

                    
//192.168.2.100:6379宕机，待恢复
# +sdown slave 192.168.2.100:6379 192.168.2.100 6379 @ mymaster 192.168.2.200 6379

                    