#!/usr/bin/env bash


docker build -t only-dblog -f only-dblog-Dockerfile .

docker run -d -p 0.0.0.0:8000:8000 \
   --restart=always \
   --name only-dblog \
   --net="host" \
   only-dblog