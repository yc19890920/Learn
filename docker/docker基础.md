1. 获取镜像
    docker pull [选项] [Docker Registry 地址[:端口号]/]仓库名[:标签]
    docker pull ubuntu:18.04
    
2. 运行
    docker run -it --rm ubuntu:18.04 bash
    
    docker run -it --rm \
    ubuntu:18.04 \
    bash
```
-it：这是两个参数，一个是 -i：交互式操作，一个是 -t 终端。我们这里打算进入 bash 执行一些命令并查看返回结果，因此我们需要交互式终端。
--rm：这个参数是说容器退出后随之将其删除。默认情况下，为了排障需求，退出的容器并不会立即删除，
      除非手动 docker rm。我们这里只是随便执行个命令，看看结果，不需要排障和保留结果，因此使用 --rm 可以避免浪费空间。
ubuntu:18.04：这是指用 ubuntu:18.04 镜像为基础来启动容器。
bash：放在镜像名后的是 命令，这里我们希望有个交互式 Shell，因此用的是 bash。
```
    

3. 利用 commit 理解镜像构成(保存镜像)   慎用 docker commit
    docker commit [选项] <容器ID或容器名> [<仓库名>[:<标签>]]
    
    docker commit \
    --author "Tao Wang <twang2218@gmail.com>" \
    --message "修改了默认网页" \
    webserver \
    nginx:v2

