#!/usr/bin/env bash


docker build -t only-dblog -f only-dblog-Dockerfile .

docker run -d -p 8000:8000 \
   --restart=always \
   --name only-dblog \
   only-dblog