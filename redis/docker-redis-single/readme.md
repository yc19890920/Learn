3.启动redis
因为从docker中拉取的redis：3.2 的镜像默认是无配置启动的，所以我们需要让他用配置启动 
redis.conf 中daemonize=NO。非后台模式，如果为YES 会的导致 redis 无法启动，因为后台会导致docker无任务可做而退出。
```
docker run -p 6380:6379 \ 
    --restart=always \
    -v /home/python/data/redis/data:/data \
    -v /home/python/Learn/redis/docker-redis-single/redis.conf:/etc/redis/redis.conf \ 
    -d redis:3.0.6 \
    redis-server /etc/redis/redis.conf  --appendonly yes --name redis-1

docker run -p 6378:6379 \
    --name redis01 \
    -v /home/python/Learn/redis/docker-redis-single/redis.conf:/etc/redis/redis.conf \
    -v /home/python/data/redis/data:/data \
    -d redis:3.0.6 \
    redis-server /etc/redis/redis.conf --appendonly yes
```

-p 6379:6379:把容器内的6379端口映射到宿主机6379端口 
-v /docker_data/redis/redis.conf:/etc/redis/redis.conf：把宿主机配置好的redis.conf放到容器内的这个位置中 
-v /docker_data/redis/data:/data：把redis持久化的数据在宿主机内显示，做数据备份 
redis-server /etc/redis/redis.conf：这个是关键配置，让redis不是无配置启动，而是按照这个redis.conf的配置启动 
--appendonly yes：redis启动后数据持久化

1. -p 6379:6379  容器redis 端口6379 映射 宿主机未6379
2. --name redis01 容器 名字 为 redis01
3. -v /root/redis/redis01/conf/redis.conf:/etc/redis/redis.conf   容器 /etc/redis/redis.conf 配置文件 映射宿主机 /root/redis/redis01/conf/redis.conf。  会将宿主机的配置文件复制到docker中。
 重要： 配置文件映射，docker镜像redis 默认无配置文件。
4 -v /root/redis/redis01/data:/data  容器 /data 映射到宿主机 /root/redis/redis01/data
5.-d redis  后台模式启动 redis 
6. redis-server /etc/redis/redis.conf    redis 将以 /etc/redis/redis.conf 为配置文件启动
7. --appendonly yes  开启redis 持久化

上传私有仓库：
docker tag redis 192.168.1.2:5000/redis:latest
docker push 192.168.1.2:5000/redis:latest

docker exec -it redis01  redis-cli
