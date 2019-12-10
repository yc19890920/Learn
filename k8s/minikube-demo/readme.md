- [Docker 和 Kubernetes 从听过到略懂：给程序员的旋风教程](https://juejin.im/post/5b62d0356fb9a04fb87767f5)


构建镜像
docker build -t yc/docker-nginx:v1 -f Dockerfile .
docker build -t yc/k8s-nginx:v1 -f Dockerfile.k8s .

运行
docker run --name webserver -d -p 81:80 yc/docker-nginx:v1
docker run --name webserver -d -p 82:80 yc/k8s-nginx:v1



## 部署一个单实例服务
$ kubectl create -f pod.yml
pod "k8s-demo" created

$ kubectl describe pods | grep Labels
Labels:		app=k8s-demo

$ kubectl get pods
NAME       READY     STATUS    RESTARTS   AGE
k8s-demo   1/1       Running   0          5s

$ kubectl create -f svc.yml
service "k8s-demo-svc" created

$ kubectl service k8s-demo-svc --url
$ kubectl describe services k8s-demo-svc
http://192.168.64.4:30050


kubectl get pods --selector="run=load-balancer-example" --output=wide

$ kubectl delete pod k8s-demo
pod "k8s-demo" deleted

$ kubectl create -f deployment.yml
deployment "k8s-demo-deployment" created

$ kubectl get rs
NAME                             DESIRED   CURRENT   READY     AGE
k8s-demo-deployment-774878f86f   10        10        10        19s

$ kubectl apply -f deployment.yml --record=true
deployment "k8s-demo-deployment" configured