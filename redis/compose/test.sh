#!/usr/bin/env bash


MASTER_IP=$(docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-master)
SLAVE_IP=$(docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' compose_redis-slave_1)
SENTINEL_IP=$(docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' compose_redis-sentinel_1)

docker exec redis-master redis-cli -p 6379 info Replication
echo " ------------------------------------------------"
sleep 2

docker exec compose_redis-sentinel_1 redis-cli -p 26379 info Sentinel
echo " ------------------------------------------------"
sleep 2

echo " ------------------------------------------------"
echo "Redis master: $MASTER_IP"
echo "Redis Slave: $SLAVE_IP"
echo " ------------------------------------------------"
echo Initial status of sentinel
echo " ------------------------------------------------"
docker exec compose_redis-sentinel_1 redis-cli -p 26379 info Sentinel
echo "Current master is"
docker exec compose_redis-sentinel_1 redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster
echo "------------------------------------------------"

echo "Stop redis master"
docker pause redis-master
echo "Wait for 60 seconds"
sleep 60
echo "Current infomation of sentinel"
docker exec compose_redis-sentinel_1 redis-cli -p 26379 info Sentinel
echo "Current master is"
docker exec compose_redis-sentinel_1 redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster


echo "------------------------------------------------"
echo "Restart Redis master"
docker unpause redis-master
sleep 5
echo "Current infomation of sentinel"
docker exec compose_redis-sentinel_1 redis-cli -p 26379 info Sentinel
echo "Current master is"
docker exec compose_redis-sentinel_1 redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster

