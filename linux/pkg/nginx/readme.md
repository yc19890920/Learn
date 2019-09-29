- [nginx的编译安装参数](https://www.jianshu.com/p/f463d92b57b7)
- [centos下Yum安装 Nginx](https://www.cnblogs.com/HKUI/p/5225895.html)

nginx源码安装configure命令的参数：
```
–prefix=path
设置安装目录，默认为/usr/local/nginx
–sbin-path=path
设置nginx可执行文件的路径和名称，默认–prefix/sbin/nginx，一般采用默认(如：–sbin-path=/home/nginx1)
–conf-path
设置nginx.conf配件文件的路径，类似–sbin-path参数，默认指定–prefix/conf/nginx.conf(/home/nginx/nginx1.conf)。nginx启动时可以通过-c参数指定配件文件。
–pid-path=path
设置存储主进程id的文件名称，默认为–prefix/logs/nginx.pid，安装完成以后，该名称也可以通过pid指令在nginx.conf配件文件中更改。
–error-log-path=path
设置主请求的错误、警告、诊断的日志文件的名称，默认为–prefix/logs/access.log，安装完成后也可以在nginx.conf配件总指定error_log指令来修改。
–http-log-path=path
设置HTTP服务器的主请求的日志文件的名称，默认为–prefix/logs/access.log。该名称也可以在nginx.conf配置文件中通过access_log指令更改。
–user=name
设置工作进程使用的非特权用户的用户名，默认为nobody。安装完成后可以在nginx.conf中通过user指令修改。
–group=name
设置工作进程使用的非特权用户组的名称，默认组名和–user的名称一致。安装完成后可以在nginx.conf配置文件中通过user指令指定。
–with-select-module、–without-select-module
启用或者禁用一个模块
–without-http_gzip_module
禁用构建gzip压缩模块。构建和运行该模块需要zlib库。
–without-http_rewrite_module
禁止构建允许HTTP服务器重定向和变更请求URI的模块。构建和运行该模块需要PCRE库。
–without-http_proxy_module
禁用HTTP服务器代理模块
–with-http_ssl_module
启用添加HTTPS协议支持到HTTP服务器的模块，该模块默认不启用。构建和运行该模块需要OpenSSL库。
–with-pcre=path
设置PCRE库的路径，该库需要从PCRE网站下载。location指令的正则表达支持需要该库。
–with-zlib=path
设置zlib库的路径，ngx_http_gzip_module模块需要该库。
更多其他参数，具体可参看nginx安装目录下configure命令的帮助文档：

./configure --help
  --help                             print this message
  --prefix=PATH                      set installation prefix
  --sbin-path=PATH                   set nginx binary pathname
  ...
  
  
--prefix=/etc/nginx 
--sbin-path=/usr/sbin/nginx 
--conf-path=/etc/nginx/nginx.conf 
--error-log-path=/var/log/nginx/error.log 
--http-log-path=/var/log/nginx/access.log 
--pid-path=/var/run/nginx.pid 
--lock-path=/var/run/nginx.lock 
--http-client-body-temp-path=/var/cache/nginx/client_temp 
--http-proxy-temp-path=/var/cache/nginx/proxy_temp 
--http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp 
--http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp 
--http-scgi-temp-path=/var/cache/nginx/scgi_temp 
--user=nginx 
--group=nginx 
--with-http_ssl_module 
--with-http_realip_module 
--with-http_addition_module 
--with-http_sub_module 
--with-http_dav_module 
--with-http_flv_module 
--with-http_mp4_module 
--with-http_gunzip_module 
--with-http_gzip_static_module 
--with-http_random_index_module 
--with-http_secure_link_module 
--with-http_stub_status_module 
--with-http_auth_request_module 
--with-mail 
--with-mail_ssl_module 
--with-file-aio --with-ipv6 
--with-http_spdy_module 
--with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic'

```