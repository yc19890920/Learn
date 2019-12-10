#!/usr/bin/env bash

ufw disable

swapoff -a

mkdir -p /home/python/.kube
cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
chown -R python:python /home/python/.kube/config

export KUBECONFIG=/etc/kubernetes/admin.conf

sysctl net.bridge.bridge-nf-call-iptables=1

kubectl apply -f /home/python/Learn/k8s/install/kube-flannel-rbac.yml
kubectl apply -f /home/python/Learn/k8s/install/kube-flannel.yml

kubectl taint nodes --all node-role.kubernetes.io/master-
