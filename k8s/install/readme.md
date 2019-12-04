角色 	主机名 	        IP地址
Master 	ubuntu-master 	192.168.181.130
Slave 	ubuntu-1 	    192.168.181.133


## 准备工作
默认方式安装Ubuntu Server 版本 16.04
配置主机名映射，每个节点
```
# cat /etc/hosts
127.0.0.1    localhost
192.168.181.130   ubuntu-master
192.168.181.133   ubuntu-1
```
如果连接gcr网站不方便，无法下载镜像，会导致安装过程卡住，可以下载我导出的镜像包，我导出的镜像网盘链接（https://pan.baidu.com/s/1ZJFRt_UNCQvwcu9UENr_gw），
解压缩以后是多个个tar包，使用docker load< xxxx.tar 导入各个文件即可）。

## 在所有节点上安装kubeadm
查看apt安装源如下配置，使用阿里云的系统和kubernetes的源。
```
$ cat /etc/apt/sources.list
# 系统安装源
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted
deb http://mirrors.aliyun.com/ubuntu/ xenial universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
deb http://mirrors.aliyun.com/ubuntu/ xenial multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
# kubeadm及kubernetes组件安装源
deb https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial main
```

安装docker，可以使用系统源的的docker.io软件包，版本1.13.1，我的系统里是已经安装好最新的版本了。

更新源，可以不理会gpg的报错信息。
```
sudo apt-get update
```

强制安装kubeadm，kubectl，kubelet软件包。
```
sudo apt-get install -y kubelet kubeadm kubectl --allow-unauthenticated
```

kubeadm安装完以后，就可以使用它来快速安装部署Kubernetes集群了。


## 使用kubeadm安装Kubernetes集群
在做好了准备工作之后，下面介绍如何使用 kubeadm 安装 Kubernetes 集群，我们将首先安装 master 节点，然后将 slave 节点一个个加入到集群中去。


使用kubeadmin初始化master节点

因为使用要使用canal，因此需要在初始化时加上网络配置参数,
设置kubernetes的子网为10.244.0.0/16，注意此处不要修改为其他地址，因为这个值与后续的canal的yaml值要一致，如果修改，请一并修改。

这个下载镜像的过程涉及翻墙，因为会从gcr的站点下载容器镜像。。。（如果大家翻墙不方便的话，可以用我在上文准备工作中提到的导出的镜像）。

如果有能够连接gcr站点的网络，那么整个安装过程非常简单。
```
kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=192.168.181.130

kubeadm init --image-repository registry.aliyuncs.com/google_containers  --kubernetes-version=v1.16.0  --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=192.168.181.130
```

如果希望 kubectl 可以以非 root 权限运行，执行命令：
执行如下命令来配置kubectl。
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```                                                                                 
这样master的节点就配置好了，并且可以使用kubectl来进行各种操作了，根据上面的提示接着往下做，将slave节点加入到集群。



```  
4.kubeadm init 初始化
执行时出现以下错误原因是被墙所以无法下载，需自己通过其他渠道下载

kubeadm init \
    --image-repository registry.aliyuncs.com/google_containers \
    --kubernetes-version=v1.16.0 \
    --pod-network-cidr=10.244.0.0/16 \
    --service-cidr=10.96.0.0/12 \
    --apiserver-advertise-address=192.168.181.130

error execution phase preflight: [preflight] Some fatal errors occurred:
	[ERROR ImagePull]: failed to pull image k8s.gcr.io/kube-apiserver:v1.14.0: output: Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
, error: exit status 1
	[ERROR ImagePull]: failed to pull image k8s.gcr.io/kube-controller-manager:v1.14.0: output: Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
, error: exit status 1
	[ERROR ImagePull]: failed to pull image k8s.gcr.io/kube-scheduler:v1.14.0: output: Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
, error: exit status 1
	[ERROR ImagePull]: failed to pull image k8s.gcr.io/kube-proxy:v1.14.0: output: Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
, error: exit status 1
	[ERROR ImagePull]: failed to pull image k8s.gcr.io/pause:3.1: output: Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
, error: exit status 1
	[ERROR ImagePull]: failed to pull image k8s.gcr.io/etcd:3.3.10: output: Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
, error: exit status 1
	[ERROR ImagePull]: failed to pull image k8s.gcr.io/coredns:1.3.1: output: Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)


手动下载镜像 这里根据自己需求下载版本

docker pull mirrorgooglecontainers/kube-apiserver:v1.14.0
docker pull mirrorgooglecontainers/kube-controller-manager:v1.14.0
docker pull mirrorgooglecontainers/kube-scheduler:v1.14.0
docker pull mirrorgooglecontainers/kube-proxy:v1.14.0
docker pull mirrorgooglecontainers/pause:3.1
docker pull mirrorgooglecontainers/etcd:3.3.10
docker pull coredns/coredns:1.3.1

修改镜像描述

docker tag mirrorgooglecontainers/kube-apiserver:v1.14.0   k8s.gcr.io/kube-apiserver:v1.14.0
docker tag mirrorgooglecontainers/kube-controller-manager:v1.14.0   k8s.gcr.io/kube-controller-manager:v1.14.0
docker tag mirrorgooglecontainers/kube-scheduler:v1.14.0   k8s.gcr.io/kube-scheduler:v1.14.0
docker tag mirrorgooglecontainers/kube-proxy:v1.14.0   k8s.gcr.io/kube-proxy:v1.14.0
docker tag mirrorgooglecontainers/pause:3.1   k8s.gcr.io/pause:3.1
docker tag mirrorgooglecontainers/etcd:3.3.10   k8s.gcr.io/etcd:3.3.10
docker tag coredns/coredns:1.3.1   k8s.gcr.io/coredns:1.3.1
```  

## Slave节点加入集群
在slave节点执行如下的命令,将slave节点加入集群，正常的返回信息如下：
```
kubeadm join 192.168.181.130:6443 --token jk8r5b.tr0d1xxvwll6odx4 --discovery-token-ca-cert-hash sha256:b68b310911d6e72cfb679d15196ad6ab5725a87e303f962e8aa4b4006d7b5ab1 
```