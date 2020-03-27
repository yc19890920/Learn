
## Nginx 高性能

Nginx可以提供HTTP服务，包括处理静态文件，支持SSL(提高HTTPS访问)、GZIP(网页压缩)、虚拟主机、URL重写等功能，可以搭配FastCGI、Gunicorn处理动态请求。
正则表达式、HTTP协议、访问控制、日志管理、虚拟主机、Web服务器搭建、反向代理、负载均衡、缓存、
以及一些常用模块和应用（包括调试输出、网页压缩、重写、重定向、防盗链、HTTPS等）

Nginx配置优化、LNMP分布式集群和高可用方案的部署、Nginx+Keepalived高可用。

1. 正则表达式、HTTP协议

2. Nginx安装

3. Nginx配置

4. Web服务器搭建

5. 负载均衡与缓存（反向代理、负载均衡、缓存配置）

6. 模块配置应用

7. 高可用负载均衡集群。


## 4. Nginx配置
学习目标
- 了解Nginx 配直文件结构；
- 掌握目录配置和访问控制；
- 熟悉日志文件的配直与切割；
- 掌握虚拟主机的配置。

打开nginx.conf 配置文件，从整体结构可以看出，该配置文件主要由以下几部分组成：
```
main
events ( ... )
http {
       server {
           location ( ... )
}
```

从上面的结构可以看出， Nginx 的默认主配置文件主要由main 、events 、http 、server 和location 5 个块组成，关于各个块的作用，详见表所示：
并且对于嵌套块（如http 、server 、location ）中的指令，执行的顺序为从外到内依次执行，
内层块中的大部分指令会自动获取外层块指令的值作为默认值，只有某些特殊指令除外。

| 块        | 说明 |
| ---     | --- |
| main	    | 主要控制 Nginx子进程所属的用户和用户组、派生子进程数、错误日志位置与级别、 pid位置、子进程优先级、进程对应CPU、进程能够打开的文件描述符数目等 | 
| events	| 控制 Nginx处理连接的方式  | 
| http	    | Nginx处理http请求的主要配置块，大多数配置都在这里面进行 | 
| server	| Nginx中主机的配置块，可用于配置多个虚拟主机  | 
| location	| server中对应目录级别的控制块，可以有多个| 

nginx.conf配置文件中默认指令：

| 指令	| 说明  | 
| ---             | --- |
| worker_processes 	 | 配置 Nginx的工作进程数，一般设为 CPU总核数或者总核数的两倍   | 	 
| worker 	         | connections 	配置 Nginx允许单个进程并发连接的最大请求数   | 
| include 	         | 用于引入配置文件 	   | 
| defaul_type	     | 设置默认文件类型 	   | 
| sendfile 	         | 默认值为 on，表示开启高效文件传输模式 	   | 
| keepalive_timeout  | 设置长连接超时时间（单位：秒） 	  |  
| listen 	         | 监听端口，默认监听 80端口 	   | 
| server_name        | 设置主机域名   | 
| root 	             | 设置主机站点根目录地址 	   | 
| index 	         | 指定默认索引文件   | 
| error_page 	     | 自定义错误页面	   | 
以上就是 nginx.conf配置文件中默认指令的相关说明，读者了解即可。	 


## 4. Web服务器搭建
- 1. FastCGI + NGINX
- 2. Nginx + Apache2
- 3. Gunicorn + Nginx
- 4. OpenResty

OpenResty 安装
```
    # import our GPG key:
    wget -qO - https://openresty.org/package/pubkey.gpg | sudo apt-key add -

    # for installing the add-apt-repository command
    # (you can remove this package and its dependencies later):
    sudo apt-get -y install software-properties-common

    # add the our official APT repository:
    sudo add-apt-repository -y "deb http://openresty.org/package/ubuntu $(lsb_release -sc) main"

    # to update the APT index:
    sudo apt-get update

Then you can install a package, say, openresty, like this:

    sudo apt-get install openresty

This package also recommends the openresty-opm and openresty-restydoc packages so the latter two will also automatically get installed by default. 
If that is not what you want, you can disable the automatic installation of recommended packages like this:

    sudo apt-get install --no-install-recommends openresty
```

## 5. 负载均衡与缓存（反向代理、负载均衡、缓存配置）

学习目标
· 掌握反向代理与负载均衡的原理及配置；
． 掌握缓存的不同实现方式；
· 了解邮件服务配直相关指令。


### 5.1 代理和反向代理

反向代理服务配置：
最主要的指令就是proxy_pass，用于设置后端服务器的地址。
```
        location / {
                proxy_pass_header Server;
                proxy_set_header Host $http_host;
                proxy_redirect off;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Scheme $scheme;
                # proxy_pass http://django_gun;
                # 二者用一个即可
                proxy_pass http://127.0.0.1:9999;
        }

```

### 5.2 负载均衡

通过Nginx 中的upstream 指令可以实现负载均衡，在该指令中能够配置负载服务器组。
目前负载均衡有4 种典型的配置方式，分别为轮询方式、权重方式、ip_hash 方式，以及利用第三方模块的方式。关于每种配置方式的特点：

| 配置方式	| 说明  | 
| ---         | --- |
| 轮询方式	    | 负载均衡默认设置方式，每个请求按照时间顺序逐一分配到不同的后端服务器进行处理，如果有服务器容机，会自动剔除  | 
| 权重方式	    | 利用weight 指定轮询的权重比率，与访问率成正比，用于后端服务器性能不均的情况  | 
| ip_hash 方式	| 每个请求按访问IP 的hash 结果分配，这样可以使每个访客固定访问一个后端服务器，可以解决Session共享的问题  | 
| 第三方模块	| 第三方模块采用fair 时，按照每台服务器的响应时间来分配请求，响应时间短的优先分配；若第三方模块采用url_hash 时，按照访问url 的hash 值来分配请求  | 

在upstream 指定的服务器组中，若每个服务器的权重都设置为1 （默认值）时，表示当前的负载均衡是一般轮询方式。
另外， Nginx 本身不包含第三方模块的实现方式，如fair 或url_hash 等，在使用时必须下载对应的upstream_fair 模块或安装hash 软件包，
才可以实现第三方模块提供的负载均衡配置。

- 1. 一般轮询负载均衡
1）准备服务器
准备3 台虚拟机，并全部安装Nginx 服务器。其中，IP 为192.168.78.3 的服务器用作负载均衡服务器，另外两台用作后端Web服务器， IP 分别为192.168.78.128 和192.168.78.200

2）配置一般轮询负载均衡
```
＃配置域名为test.ng.test 的虚拟主机
server {
    listen 80;
    server_name test.ng.test;
    location / {
        proxy_pass http://web_server;
    }
}

＃配置负载均衡服务器组
upstream web_server {
    server 192.168.78.128;
    server 192.168.78.200;
}
```

- 2. 加权轮询负载均衡
如果负载均衡服务器组中的服务器硬件配置强弱不一，则可以通过weight 参数设置权重大小。
对于配置较好的服务器，可以为其设置成比较高的权值，对于配置较差的服务器，可以为其分配较小的权值。
通过加权轮询，可以让每台服务器承担与之硬件配置相符的工作量，从而在整体上发挥最佳的效果。

```
upstream web_server {
    server 192.168.78.128 weight=1;
    server 192.168.78.200 weight=3;
}

upstream web_server {
    server 192.168.78.128 weight=l max_fails=1 fail_timeout=2;
    server 192.168.78.200 weight=3 max_fails=2 fail_timeout=2;
    server 192.168.78.201 backup;
```

- 3. ip_hash负载均衡
ip_hash 方式的负载均衡，是将每个请求按照访问IP 的hash 结果分配，这样就可以便来自同一个IP 的客户端用户固定访问一台Web 服务器，
有效地解决了动态网页存在的Session 共享问题。下面将上述负载均衡服务器组的设置修改成如下形式：
```
upstream web_server {
ip_hash;
    server 192.168.78.128;
    server 192.168.78.200;
    server 192.168.78.3 down;
}
```
在上述配置中， upstream 块中的ip_hash 指令用于标识当前负载均衡的处理方式。
其中，对于一个暂时性者机的服务器，可以使用down 参数标识出来，这样在负载均衡时，就会忽略该服务器的分配。
需要注意的是，在使用ip_ hash 方式处理负载均衡时，Web 服务器在负载均衡列表中的状态不能使用weight 和backup 设置。

值得一提的是，由于ip_hash 方式为每一个用户IP 绑定一个Web 服务器处理，将会导致某些Web 服务器接收的请求多，
某些Web 服务器接到的请求少，无法保证Web 服务器的负载均衡。因此，建议只在必要的情况下使用这种方式。

- 4. 利用第三方模块 nginx-upstream-fair

```
＃配置域名为test.ng.test 的虚拟主机
server {
    listen 80;
    server_name test.ng.test;
    location / {
        proxy_pass http://web_server;
    }
}
＃配置fair 方式的负载均衡
upstream web_server {
    server 192.168.78.128;
    server 192.168.78.200;
    fair ;
}
```

### 5.3 缓存配置
对于一个含有大量内容的网站来说，随着访问量的增多，对于经常被用户访问的内容，若每一次都要到后端服务器中获取，会给服务器造成很大的压力。
为此，利用反向代理服务器对访问频率较多的内容进行缓存，有利于节省后端服务器的资源。
Nginx 提供了两种Web缓存方式， 一种是永久性缓存，另一种是临时性缓存。


## 6. 模块配置应用

学习目标
模块配置应用
· 了解Nginx 的模块化结构设计；
· 掌握Nginx 的调试方法及手册的使用；
· 掌握网页压缩、重写、防盗链的配置；
· 熟悉SSL 、响应内容替换的配直。

7.7 .2 颁发认证证书

- 生成服务器的RSA 私钥
RSA 是HTTPS 使用的一种算法，在配置HTTPS 前，需要先为服务器生成私钥
cd /etc/nginx/ssl
sudo openssl genrsa -out server.key 2048

- 生成服务器的CSR 证书请求文件
CSR 证书谙求文件是服务器的公钥，用于提交给CA 机构进行签名。
sudo openssl req -new -key server.key -out server.csr

- CA 为服务器认证证书
sudo openssl x509 -req -days 30 -in server.csr -signkey server.key -out server.crt

- 配置HTTPS 网站
在Nginx 服务器中配置SSL 服务，首先需要在编译安装Ng inx 时添加对ngx_http_ssl_module 模块的支持, nginx.conf配置
```
server {
    listen 443;
    server_name www.test.com;
    # root html/test.com;
    ssl on;
    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
}
```

```
server {  
    listen 80;
    listen [::]:80 ssl ipv6only=on; 
    listen 443 ssl;
    listen [::]:443 ssl ipv6only=on;
    server_name example.com;

    ssl on;
    ssl_certificate /etc/ssl/private/example_com.crt;
    ssl_certificate_key /etc/ssl/private/example_com.key;
}
```

```
# the upstream component nginx needs to connect to

upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8080; # for a web port socket (we'll use this first)
}


# configuration of the server
server {
        # the port your site will be served on
        listen      80;
        server_name  djangoblog.com;

        listen 443 ssl;
        # root html/test.com;
        ssl on;
        ssl_certificate /etc/nginx/ssl/server.crt;
        ssl_certificate_key /etc/nginx/ssl/server.key;

        #######   nginx上启用https   #######
        #ssl on;
        #ssl_certificate      /home/python/git/dblog/ssl_certs/cert.pem;#证书路径
        #ssl_certificate_key /home/python/git/dblog/ssl_certs/cert.key;#key路径

        #ssl_session_cache    shared:SSL:1m; #s储存SSL会话的缓存类型和大小                        
        #ssl_session_timeout  5m; #会话过期时间   

        #rewrite  ^/(.*)$ https://djangoblog.com/$1 permanent;  
        ######   nginx上启用https   #######


        access_log          /home/python/log/dblog_ng;
        error_log           /home/python/log/dblog_ngerr;

        proxy_connect_timeout    600;
        proxy_read_timeout       600;
        proxy_send_timeout       600;

        # max upload size
        client_max_body_size 50M;

        location ^~ /static/ {
            # your own static file
            root /home/python/git/dblog/;
            if ($query_string) {
                expires max;
            }
            #expires 30d;
            #break;
        }

        location /media/ {
            root /home/python/git/dblog/;
            expires 30d;
            break;
        }

        # Django media
        #location /media  {
        #    alias /path/to/your/mysite/media;  # your Django project's media files - amend as required
        #}

        #location /static {
        #    alias /home/python/git/dblog/static/; # your Django project's static files - amend as required
        #}

        # Finally, send all non-media requests to the Django server.
        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://django;
        }


        #-- Error page setting ---------------------------
        error_page          404              /404.html;
        error_page          500 502 503 504  /50x.html;
        location = /50x.html {
                 root            /home/python/git/dblog/templates/errpage;
        }
        location = /404.html {
                 root            /home/python/git/dblog/templates/errpage;
        }
}
```

```
默认情况下ssl模块并未被安装，如果要使用该模块则需要在编译时指定–with-http_ssl_module参数，安装模块依赖于OpenSSL库和一些引用文件，通常这些文件并不在同一个软件包中。通常这个文件名类似libssl-dev。
生成证书

可以通过以下步骤生成一个简单的证书：
首先，进入你想创建证书和私钥的目录，例如：

    $ cd /usr/local/nginx/conf

创建服务器私钥，命令会让你输入一个口令：

    $ openssl genrsa -des3 -out server.key 1024

创建签名请求的证书（CSR）：

    $ openssl req -new -key server.key -out server.csr

在加载SSL支持的Nginx并使用上述私钥时除去必须的口令：

    $ cp server.key server.key.org
    $ openssl rsa -in server.key.org -out server.key

配置nginx

最后标记证书使用上述私钥和CSR：

    $ openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

修改Nginx配置文件，让其包含新标记的证书和私钥：

    server {
        server_name YOUR_DOMAINNAME_HERE;
        listen 443;
        ssl on;
        ssl_certificate /usr/local/nginx/conf/server.crt;
        ssl_certificate_key /usr/local/nginx/conf/server.key;
    }

重启nginx。
这样就可以通过以下方式访问：

https://YOUR_DOMAINNAME_HERE

另外还可以加入如下代码实现80端口重定向到443

server {
    listen 80;
    server_name www.centos.bz;
    rewrite ^(.*) https://$server_name$1 permanent;
}

```

## 7. 高可用负载均衡集群。
学习目标
· 掌握Nginx 的配置优化；
· 掌握LNMP 分布式集群的搭建；
· 掌握Nginx+ Keepalived 高可用方案的部署。

为了提高综合运用能力，将会针对高并发、高负载网站需求的具体实现进行讲解，包括Nginx 的配置优化、LNMP 分布式集群，以及Nginx+ Keepalived 高可用方案，利用这些技术来增强网站的性能和可靠性。

## 7.1 掌握Nginx 的配置优化；
1) 优化Nginx 连接数
```
# worker_processes auto;
worker_rlimit_nofile 65535 ;
worker_processes 8;
pid /run/nginx.pid;

events {
        worker_connections 65535;
        multi_accept on;
}
```
在上述配置中， worker_processes 指令用于指定工作进程的个数，设置为auto 时Nginx将根据CPU 的核心数来控制； 
worker_rlimit_nofile 用于设置最多打开的文件数业； worker_connections 用于设置每个工作进程可接收的连接数； 
multi_accept 表示是否允许一个工作进程响应多个请求。

2) 客户端请求限制
### 限制同一个IP 的并发数
通过limit_conn 指令可以限制并发连接数，在conf/nginx.conf 配置文件中进行如下配置即可。
```
http {
    limit_conn_zone $binary_remote_addr zone=perip:2Om;
    limit_conn perip 10;
}
```
在上述配置中， limit_conn_zone 指令用于开辟一个共享内存空间保存客户端IP ，空间名称为perip ，空间大小为lOMB; 
limit_conn 指令用于限制连接数量； 预定义变量$binary_remote_addr 保存了用二进制表示的当前客户端IP 地址。
上述配置生效后， Nginx 将对于同一个IP 地址只允许10 个并发连接，当超过时返回503 （服务暂时不可用）错误。
另外，limit_conn 指令也可以在server 和l ocation 块中使用，用于实现不同级别的控制。

### 限制虚拟主机的并发数
在使用limit_conn_zone 指令时，也可以用共享内存空间保存虚拟主机名（ $server_name ），实现对虚拟主机的并发数进行限制，具体配置如下。
```
http {
    limit_conn_zone $binary_remote_addr zone=perip:2Om;
    limit_conn_zone $server_name zone=perserver:10m;
    limit_conn perip 10;
    
    server {
        listen 80;
        server_name localhost;
        limit_conn perserver 20;
    }
}
```

### 限制晌应的传输速率
Nginx 的limit_rate 指令用于限制服务器在响应时传输数据到客户端的速率，可以在http 、server 、location 、location 中的if 块中使用。
```
http {
    limit_rate lOOk;
    limit_rate_after lOm;
}
```
在上述配置中， limit_rate 用于限制每个连接的传输速率（每秒lOOKB); limit_ rate_after用于在已经传输指定大小的数据后再进行限速，
从而实现只针对大文件限制下载速度。如果省略limit_rate_after 指令，则无论文件大小是多少，都会进行限速。

3) 浏览器缓存优化
服务器可以通过响应消息控制浏览器缓存，和缓存相关的响应头有Expires 、CacheControl、ETag 、Last-Modified 等。
其中， Last-Modified 和ETag 由Nginx 自动生成，前者表示最后修改的时间，后者用于浏览器判断内容有无改变； 
Cache-Control 比较复杂，通常根据实际需要进行控制；
Expires 表示该资源的过期时间，如果没有过期则浏览器不会发起HTTP 请求。
```
server {
    location ~\.(gif|jpg|jpeg|png|bmp|swf)$ {
        expires 30d;
    }
    location ~\.(css|js)$ {
        expires 12h;
    }
}
```

## 7.2 掌握LNMP 分布式集群的搭建；
集群（ cluster）是指将多台服务器集中起来一起进行同一种服务。相比一台服务器，集群的优势在于将负载均衡到每台服务器上，从而承载更多的工作量。
而且集群具有很强的可靠性，当其中一台服务器发生故障时，不会造成整个服务中断。
集群还具有成本上的优势，这是因为当一台计算机的计算能力达到一定程度时，就会产生瓶颈，即付出巨大的成本后只换来少量的性能提升。
如果利用集群架构，可以专门购置一批高性价比的服务器，用较少的成本就能得到可观的性能提升。

负载均衡服务器， 主要工作是承担网络吞吐压力，而与业务有关的计算工作分摊到多台后端服务器中。
备用服务器 监控 负载均衡服务器

分布式和集群都是为提高服务器处理能力而设计的，其区别是集群由多台服务器共同完成一件工作，而分布式是将工作进行业务拆分，然后由多种不同的服务器进行处理。
集群是一种串行的工作方式，虽然服务器数量多，但是对客户端而言只有其中一台服务器处理了请求；
而分布式是一种并行的工作方式，由于业务是拆分的，客户端需要向多台服务器发送请求，每个服务器各司其责才能完成任务。
从上述描述可以看出，分布式和集群各有优缺点，但对于规模庞大的网站来说，可以选取两者的优点，将业务拆分到多个集群中，形成分布式集群架构。


### 安装和启动NFS 服务

sudo apt-get install nfs-kernel-server

配置：/etc/exports
/home 192.168.1.0/24(rw,sync,no_root_squash)

启动：
sudo /etc/init.d/nfs-kernel-server restart
service nfs-server restart


配置共享目录：
sudo mkdir -p /data/nfsshare

查看NFS 服务器巾的共享目录
showmount -e localhost
showmount -e 192.168.1.24


### Nginx+ Keepalived 高可用方案