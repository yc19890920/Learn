## swap分区的关闭
sudo swapoff -a
swap分区的开启
sudo swapon -a

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

apt-get update
sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni --allow-unauthenticated

kubeadm init  --image-repository registry.aliyuncs.com/google_containers  --kubernetes-version=v1.16.0  --pod-network-cidr=10.244.0.0/16
日志：
```
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.1.24:6443 --token cdet2e.tmawp9xzh6yeo1h7 \
    --discovery-token-ca-cert-hash sha256:966304896a2e0e3999b424f7ef930ba0c25907caf85d2a715ed14a3b01141ade 
```

## vim ~/.bashrc 
```
export KUBECONFIG=/etc/kubernetes/admin.conf

export KUBECONFIG=$HOME/.kube/config
```
source ~/.bashrc 

## 初始化kubectl配置之后
kubectl get nodes
居然是NotReady状态！！

查看以下pods的状态，发现kube-dns 还在挂起，怪不得docker images的时候没有发现kube-dns镜像
kubectl get pods --all-namespaces

## 安装Pod Network
export KUBECONFIG=/etc/kubernetes/admin.conf
export KUBECONFIG=/home/python/.kube/config 

sysctl net.bridge.bridge-nf-call-iptables=1

kubectl apply -f kube-flannel-rbac.yml
kubectl apply -f kube-flannel.yml


## Slave节点加入集群
kubeadm join 192.168.1.24:6443 --token uth736.zovx1ylensd8ygcj --discovery-token-ca-cert-hash sha256:6dacc6f33ce155b019dc32323874fed4d25657fde6503f2d0e46a72f0c477625 


这里搭建的是测试环境可以使用下面的命令使Master Node参与工作负载：
kubectl taint nodes --all node-role.kubernetes.io/master-
kubectl taint nodes $(hostname) node-role.kubernetes.io/master:NoSchedule-

使用kubeadm初始化的集群，出于安全考虑Pod不会被调度到Master Node上，可使用如下命令使Master节点参与工作负载

kubectl taint nodes --all node-role.kubernetes.io/master-


Here we will use Calico as the network of choice:
kubectl apply -f https://docs.projectcalico.org/v3.7/manifests/calico.yaml

Allow a single-host cluster
Kubernetes is about multi-host clustering — so by default containers cannot run on master nodes in the cluster. 
Since we only have one node — we’ll taint it so that it can run containers for us.
$ kubectl taint nodes --all node-role.kubernetes.io/master-


## 部署 Hello World 应用
kubectl run hello-world --replicas=1 --labels="run=load-balancer-example" --image=gcr.io/google-samples/node-hello:1.0  --port=8008

--replicas=1表示我们创建的 Pod 数量为 1，--port=8080是容器的端口，并不是外部访问的端口。

创建好之后，我们可以通过下面几个命令，查看部署的信息和进度：
```
$ kubectl get deployments hello-world
$ kubectl describe deployments hello-world

$ kubectl get replicasets
$ kubectl describe replicasets
```

部署成功之后，我们还需要创建对应的 Service（类型为 NodePort）：
```
$ kubectl expose deployment hello-world --type=NodePort --name=example-service
service/example-service exposed
```

建好之后，我们查看下 Service 的信息（30496 就是对外暴露的端口）：
```
root@python-virtual-machine:/home/python/Learn/k8s/install# kubectl describe services example-service
Name:                     example-service
Namespace:                default
Labels:                   run=load-balancer-example
Annotations:              <none>
Selector:                 run=load-balancer-example
Type:                     NodePort
IP:                       10.111.131.99
Port:                     <unset>  8008/TCP
TargetPort:               8008/TCP
NodePort:                 <unset>  30496/TCP
Endpoints:                
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

我们还可以查看 Pod 的信息：
```
$ kubectl get pods --selector="run=load-balancer-example" --output=wide
NAME                          READY     STATUS    RESTARTS   AGE       IP           NODE
hello-world-58f9949f8-c28gx   1/1       Running   0          15m       10.244.3.8   worker1
```

然后，我们就可以浏览器直接打开（http://10.9.10.152:31860/），10.9.10.152是 worker1 的 IP 地址，或者直接测试访问命令：
$ curl http://10.244.0.4:30496/
Hello Kubernetes!

另外，说明下 Kubernetes 三种暴露服务的方式：
LoadBlancer Service：LoadBlancer Service 是 kubernetes 深度结合云平台的一个组件；当使用 LoadBlancer Service 暴露服务时，实际上是通过向底层云平台申请创建一个负载均衡器来向外暴露服务；目前 LoadBlancer Service 支持的云平台已经相对完善，比如国外的 GCE、DigitalOcean，国内的 阿里云，私有云 Openstack 等等，由于 LoadBlancer Service 深度结合了云平台，所以只能在一些云平台上来使用。
NodePort Service：NodePort Service 顾名思义，实质上就是通过在集群的每个 node 上暴露一个端口，然后将这个端口映射到某个具体的 service 来实现的，虽然每个 node 的端口有很多(0~65535)，但是由于安全性和易用性(服务多了就乱了，还有端口冲突问题)实际使用可能并不多。
Ingress：Ingress 这个东西是 1.2 后才出现的，通过 Ingress 用户可以实现使用 nginx 等开源的反向代理负载均衡器实现对外暴露服务。
