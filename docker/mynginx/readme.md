nginx Dockerfile


构建镜像
docker build -t yc/nginx:v1 .


运行
docker run --name webserver -d -p 83:80 yc/nginx:v1

