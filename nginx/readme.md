docker run –d –it –v /opt/dockerconf/nginx/nginx.conf:/etc/nginx/nginx.conf –name nginx-master –p 80:80 nginx

docker container run \
  -d \
  -p 88:80 \
  --rm \
  --name mynginx \
  -v "$PWD/html":/usr/share/nginx/html \
  nginx
  
## 拷贝配置
docker container cp mynginx:/etc/nginx .
mv nginx conf
docker container stop mynginx

## 映射配置目录
docker container run \
  --rm \
  --name mynginx \
  -v "$PWD/html":/usr/share/nginx/html \
  -v "$PWD/conf":/etc/nginx \
  -p 127.0.0.2:8080:80 \
  -d \
  nginx