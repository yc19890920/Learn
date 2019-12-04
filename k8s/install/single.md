- [Kubeadm 安装部署 Kubernetes 集群](https://www.cnblogs.com/xishuai/p/install-kubernetes-on-ubuntu-with-kubeadm.html)
- [ubuntu16.04 kubeadm快速搭建kubernetes环境](https://blog.csdn.net/oqqYuan1234567890/article/details/74080155)
- [使用kubeadm安装Kubernetes 1.6](https://blog.frognew.com/2017/04/kubeadm-install-kubernetes-1.6.html)
- [使用kubeadm 部署 Kubernetes(国内环境)](https://juejin.im/post/5b8a4536e51d4538c545645c)
- [使用kubeadm安装Kubernetes 1.6](https://blog.frognew.com/2017/04/kubeadm-install-kubernetes-1.6.html)

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

kubeadm join 192.168.1.24:6443 --token uth736.zovx1ylensd8ygcj \
    --discovery-token-ca-cert-hash sha256:6dacc6f33ce155b019dc32323874fed4d25657fde6503f2d0e46a72f0c477625 
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
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-rbac.yml
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.9.1/Documentation/kube-flannel.yml

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel.yml
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-legacy.yml

kubectl create -f https://github.com/coreos/flannel/blob/master/Documentation/k8s-manifests/kube-flannel-rbac.yml


```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-legacy.yml

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel-rbac.yml
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

kubectl create -f https://github.com/coreos/flannel/raw/master/Documentation/kube-flannel-rbac.yml
kubectl create -f  https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

