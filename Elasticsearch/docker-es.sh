#!/bin/bash

docker pull elasticsearch:6.7.0
docker stop es
docker container prune

docker run -d \
    --name es \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -v $(pwd)/docker-es/data:/usr/share/elasticsearch/data \
    elasticsearch:6.7.0

Ret=$?
echo $Ret
exit $Ret