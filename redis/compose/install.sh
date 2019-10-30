#!/usr/bin/env bash

docker-compose up -d

sleep 1
docker-compose scale redis-slave=2

sleep 1
docker-compose scale redis-sentinel=3


docker ps -a
