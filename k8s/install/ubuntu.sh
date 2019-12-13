#!/usr/bin/env bash

ufw disable

swapoff -a

# kubeadm init  --image-repository registry.aliyuncs.com/google_containers  --kubernetes-version=v1.16.0  --pod-network-cidr=10.244.0.0/16

# sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni --allow-unauthenticated
# kubeadm init  --image-repository registry.aliyuncs.com/google_containers  --kubernetes-version=v1.17.0  --pod-network-cidr=10.244.0.0/16

mkdir -p /home/python/.kube
cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
chown -R python:python /home/python/.kube/config

export KUBECONFIG=/etc/kubernetes/admin.conf

sysctl net.bridge.bridge-nf-call-iptables=1

kubectl apply -f /home/python/Learn/k8s/install/kube-flannel-rbac.yml
kubectl apply -f /home/python/Learn/k8s/install/kube-flannel.yml

kubectl taint nodes --all node-role.kubernetes.io/master-

source <(kubectl completion bash)
