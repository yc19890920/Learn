1. 列出所有的容器 ID
    docker ps -aq
    
2. 停止所有的容器
    docker stop $(docker ps -aq)
    清理停止的容器：
    docker rm -lv CONTAINER
    -l是清理link，v是清理volume。 这里的CONTAINER是容器的name或ID，可以是一个或多个。
    
    
3. 删除所有的容器
    docker rm $(docker ps -aq)
    
4. 删除所有的镜像
    docker rmi $(docker images -q)
    
5. 复制文件
```
docker cp mycontainer:/opt/file.txt /opt/local/
docker cp /opt/local/file.txt mycontainer:/opt/
```

提醒， 现在的docker有了专门清理资源(container、image、网络)的命令。 
docker 1.13 中增加了 docker system prune 的命令，针对container、image可以使用 
docker container prune
docker image prune 
命令。

6. 删除所有不使用的镜像
    docker image prune --force --all 
    或者 
    docker image prune -f -a 
   
7. 删除所有停止的容器
    docker container prune -f
    
8. 查看 Docker 的磁盘使用情况， 类似于 Linux 上的df命令
    docker system df
    
docker system prune 命令可以用于清理磁盘，删除关闭的容器、无用的数据卷和网络，以及 dangling 镜像(即无 tag 的镜像)。
docker system prune -a  命令清理得更加彻底，可以将没有容器使用 Docker 镜像都删掉。
注意，这两个命令会把你暂时关闭的容器，以及暂时没有用到的 Docker 镜像都删掉了…所以使用之前一定要想清楚吶。


9. 如何批量删除Docker中已经停止的容器
```
方法一：

#显示所有的容器，过滤出Exited状态的容器，取出这些容器的ID，

sudo docker ps -a|grep Exited|awk '{print $1}'

#查询所有的容器，过滤出Exited状态的容器，列出容器ID，删除这些容器

sudo docker rm `docker ps -a|grep Exited|awk '{print $1}'`



方法二： 

#删除所有未运行的容器（已经运行的删除不了，未运行的就一起被删除了）

sudo docker rm $(sudo docker ps -a -q)



方法三：

#根据容器的状态，删除Exited状态的容器

sudo docker rm $(sudo docker ps -qf status=exited)

 

方法四：

#Docker 1.13版本以后，可以使用 docker containers prune 命令，删除孤立的容器。

sudo docker container prune
```


10. 清理Docker的container，image与volume
```
Docker的镜像（image）、容器（container）、数据卷（volume）， 都是由daemon托管的。 因此，在需要清理时，也需要使用其自带的手段。

清理所有停止运行的容器：
docker container prune
# or
docker rm $(docker ps -aq)

清理所有悬挂（<none>）镜像：
docker image prune
# or
docker rmi $(docker images -qf "dangling=true")

清理所有无用数据卷：
docker volume prune
由于prune操作是批量删除类的危险操作，所以会有一次确认。 
如果不想输入y<CR>来确认，可以添加-f操作。慎用！
```