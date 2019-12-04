#!/usr/bin/env bash

echo "启动 Etcd 服务。"

docker run \
    --net=host \
    -d gcr.io/google_containers/etcd:2.0.9 \
    /usr/local/bin/etcd --addr=127.0.0.1:4001 --bind-addr=0.0.0.0:4001 --data-dir=/home/python/data/etcd


echo "启动主节点"

docker run --net=host -d \
    -v /var/run/docker.sock:/var/run/docker.sock  \
    gcr.io/google_containers/hyperkube:v0.17.0 \
    /hyperkube kubelet --api_servers=http://localhost:8080 \
    --v=2 --address=0.0.0.0 --enable_server --hostname_override=127.0.0.1 --config=/etc/kubernetes/manifests


echo "启动服务代理"
docker run -d --net=host --privileged gcr.io/google_containers/hyperkube:v0.17.0 \
    /hyperkube proxy --master=http://127.0.0.1:8080 --v=2


echo "测试状态: curl 127.0.0.1:8080"

curl 127.0.0.1:8080