#!/usr/bin/env bash

docker run -d \
    --restart=always  \
    --name docker-hub \
    -p 7000:5000 \
    -v `pwd`/registry:/var/lib/registry \
    -v `pwd`/auth:/auth \
    -v `pwd`/certs:/certs \
    -e "REGISTRY_AUTH=htpasswd" \
    -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
    -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
    registry

#    -v `pwd`/certs:/certs \
#    -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/myrepo.crt \
#    -e REGISTRY_HTTP_TLS_KEY=/certs/myrepo.key \


echo "用 curl 查看仓库中的镜像:"
docker login -u yc -p 1qaz@WSX 127.0.0.1:7000
# curl http://127.0.0.1:7000/v2/_catalog
docker logout 127.0.0.1:7000
# curl 127.0.0.1:7000/v2/_catalog
# 192.168.181.135:7000/v2/_catalog


:<<EOF
私有仓库认证
私有仓库搭建以后其他所有客户端均可以push、pull，docker官方提供认证方法对docker仓库进行权限保护。
我这只用的用户权限限制，官网配置是TLS和用户权限验证一起使用。

1.删除原启动的仓库容器
docker stop docker-hub
docker rm -f docker-hub

2.创建存放密码账号的文件
mkdir -p /docker-hub/auth
docker run --entrypoint htpasswd registry -Bbn testuser testpassword > auth/htpasswd
docker run --entrypoint htpasswd registry -Bbn yc 1qaz@WSX >> auth/htpasswd

3.重新启动docker-hub容器
docker run -d -p 5000:5000 --restart=always --name docker-hub \
  -v /docker-hub/registry:/var/lib/registry \
  -v /docker-hub/auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  registry

4.现在客户端再pull、push就会提示报错，无法提交，需要登录私有仓库。

登录
docker login -u testuser -p testpassword 192.168.1.163:5000
退出
docker logout 192.168.1.163:5000

认证以后无法直接在服务器查看 curl 127.0.0.1:5000/v2/_catalog 仓库的镜像，会出现报错，但是可以用浏览器访问。
EOF