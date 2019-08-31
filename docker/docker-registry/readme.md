将上传的镜像放到本地的 /opt/data/registry 目录。
```
docker run -d \
    -p 0.0.0.0:85:5000 \
    -v /home/python/Learn/docker/docker-registry:/var/lib/registry \
    --name local-registry \
    registry
```


使用 docker tag 将 ubuntu:latest 这个镜像标记为 127.0.0.1:5000/ubuntu:latest。
格式为 docker tag IMAGE[:TAG] [REGISTRY_HOST[:REGISTRY_PORT]/]REPOSITORY[:TAG]。
```
docker tag ubuntu:18.04 127.0.0.1:85/ubuntu:18.04
```

使用 docker push 上传标记的镜像。
docker push 127.0.0.1:85/ubuntu:18.04

用 curl 查看仓库中的镜像。
curl 127.0.0.1:85/v2/_catalog
