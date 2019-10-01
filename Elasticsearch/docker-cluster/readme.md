- [docker安装elasticsearch](https://juejin.im/post/5ca0d12c518825550b35be6d)
- [docker简易搭建ElasticSearch集群](https://blog.csdn.net/belonghuang157405/article/details/83301937)

docker run -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \
    -d \
    -p 9200:9200 \
    -p 9300:9300 \
    -v $(pwd)/mnt/config/es1.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
    -v $(pwd)/mnt/data1:/usr/share/elasticsearch/data \
    --name es01 \
    elasticsearch:6.7.0

## 前言
安装es么，也没什么难的，主要网上搜一搜，看看文档，但是走过的坑还是需要记录一下的
主要参考这三份文档：
- [Running the Elastic Stack on Docker](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html)
- [docker简易搭建ElasticSearch集群](https://blog.csdn.net/belonghuang157405/article/details/83301937)
- [Running Kibana on Docker](https://www.elastic.co/guide/en/kibana/6.7/docker.html)


## 安装es
直接 docker pull elasticsearch 显示没有这个tag所以去dockerhub看了下tag，加上了版本号6.7.0
拉取镜像
docker pull elasticsearch:6.7.0

复制代码创建es的挂载目录以及配置文件：
```
cd  /
mkdir-p mnt/elasticsearch
cd  mnt/elasticsearch
mkdir config
mkdir matser
mkdir slave
chmod 777 master
chmod 777 slave
```
config 里面分别放两个配置文件
```
cd config
touch master.yml
touch slave.yml
```
matser.yml
```
cluster.name: elasticsearch-cluster
node.name: master
network.bind_host: 0.0.0.0
network.publish_host: `your ip`
http.port: 9200
transport.tcp.port: 9300
http.cors.enabled: true
http.cors.allow-origin: "*"
node.master: true 
node.data: true  
discovery.zen.ping.unicast.hosts: [" `your ip`:9300"," `your ip`:9301"]
```
slave.yml
```
cluster.name: elasticsearch-cluster
node.name: slave
network.bind_host: 0.0.0.0
network.publish_host: `your ip`
http.port: 9202
transport.tcp.port: 9302
http.cors.enabled: true
http.cors.allow-origin: "*"
node.master: false
node.data: true  
discovery.zen.ping.unicast.hosts: ["`your ip`:9300","`your ip`:9301"]
```

3.ElasticSearch配置文件说明：
```
cluster.name：用于唯一标识一个集群，不同的集群，其 cluster.name 不同，集群名字相同的所有节点自动组成一个集群。如果不配置改属性，默认值是：elasticsearch。
node.name：节点名，默认随机指定一个name列表中名字。集群中node名字不能重复
index.number_of_shards: 默认的配置是把索引分为5个分片
index.number_of_replicas:设置每个index的默认的冗余备份的分片数，默认是1

bootstrap.memory_lock: true 当JVM做分页切换（swapping）时，ElasticSearch执行的效率会降低，推荐把ES_MIN_MEM和ES_MAX_MEM两个环境变量设置成同一个值，并且保证机器有足够的物理内存分配给ES，同时允许ElasticSearch进程锁住内存
network.bind_host: 设置可以访问的ip,可以是ipv4或ipv6的，默认为0.0.0.0，这里全部设置通过
network.publish_host:设置其它结点和该结点交互的ip地址，如果不设置它会自动判断，值必须是个真实的ip地址

http.port:设置对外服务的http端口，默认为9200
transport.tcp.port: 设置节点之间交互的tcp端口，默认是9300
http.cors.enabled: 是否允许跨域REST请求
http.cors.allow-origin: 允许 REST 请求来自何处
node.master: true 配置该结点有资格被选举为主结点（候选主结点），用于处理请求和管理集群。如果结点没有资格成为主结点，那么该结点永远不可能成为主结点；如果结点有资格成为主结点，只有在被其他候选主结点认可和被选举为主结点之后，才真正成为主结点。
node.data: true 配置该结点是数据结点，用于保存数据，执行数据相关的操作（CRUD，Aggregation）；
discovery.zen.minimum_master_nodes: 自动发现master节点的最小数，如果这个集群中配置进来的master节点少于这个数目，es的日志会一直报master节点数目不足。
    （默认为1）为了避免脑裂，个数请遵从该公式 => (totalnumber of master-eligible nodes / 2 + 1)。 
    * 脑裂是指在主备切换时，由于切换不彻底或其他原因，导致客户端和Slave误以为出现两个active master，最终使得整个集群处于混乱状态*
discovery.zen.ping.unicast.hosts： 集群个节点IP地址，也可以使用es-node等名称，需要各节点能够解析
```

## 调高JVM线程数限制数量（不然启动容器的时候会报错，亲身试验）
```
vim /etc/sysctl.conf
# 添加这个
vm.max_map_count=262144 
# 保存后执行这个命令
sysctl -p
```
## 初始化容器
```
master
docker run -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \
    -d \
    -p 9200:9200 \
    -p 9300:9300 \
    -v /mnt/elasticsearch/config/master.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
    -v /mnt/elasticsearch/master:/usr/share/elasticsearch/data \
    --name es-master \
    elasticsearch:6.7.0

slave
docker run -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \
    -d \
    -p 9201:9201 \
    -p 9301:9301 \
    -v /mnt/elasticsearch/config/slave.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
    -v /mnt/elasticsearch/slave:/usr/share/elasticsearch/data \
    --name es-slave \
    elasticsearch:6.7.0
```

## 校验是否安装成功
浏览器访问 http://yourip:9200


## 安装kibana
刚开始装的时候看网上的教程来，一直连不上es，直接去官网找文档了，具体如下
docker pull kibana:6.7.0
docker run --link es-master:elasticsearch -p 5601:5601 --name kibana -d kibana:6.7.0

代码访问 http://yourip:5601


## 使用compose安装7.3.1版本

因为有过经验了，直接去dockerhub上看安装教程

第一步：调线程数,详情见上面操作

第二步：编写docker-compose.yml
```
version: '2.2'
services:
  es01:
    image: elasticsearch:7.3.1
    container_name: es01
    environment:
      - node.name=es01
      - discovery.seed_hosts=es02
      - cluster.initial_master_nodes=es01,es02
      - cluster.name=docker-cluster
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - ./esdata01:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
    networks:
      - esnet
  es02:
    image: elasticsearch:7.3.1
    container_name: es02
    environment:
      - node.name=es02
      - discovery.seed_hosts=es01
      - cluster.initial_master_nodes=es01,es02
      - cluster.name=docker-cluster
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - ./esdata02:/usr/share/elasticsearch/data
    networks:
      - esnet
  kibana:
    image: kibana:7.3.1
    container_name: kibana
    ports:
      - 5601:5601
    links:
      - es01:elasticsearch ## 这里一定要跟上 :elasticsearch,不然会出错，详情看dockerhub上的kibana教程
    networks:
      - esnet  


networks:
  esnet:
```

docker-compose up -d
