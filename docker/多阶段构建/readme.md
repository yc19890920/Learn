
## 全部放入一个 Dockerfile
docker build -t go/helloworld:1 -f Dockerfile.one .


## 多阶段构建
docker build -t go/helloworld:2 .
