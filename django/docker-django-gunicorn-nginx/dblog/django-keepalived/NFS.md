
##  主服务器：
192.168.52.132

安装软件包
sudo apt-get update
sudo apt-get install nfs-kernel-server

在主机上创建共享目录
sudo mkdir -p /home/python/share
sudo chown -R nobody:nogroup /home/python/share
sudo chown -R  www-data:www-data /home/python/share
sudo chmod 777 /home/python/share

在主机服务器上配置NFS导出
sudo vim /etc/exports

/home/python/share    192.168.52.128(rw,sync,no_root_squash,no_subtree_check)
/home/python/share    192.168.52.131(rw,sync,no_root_squash,no_subtree_check)
重启NFS服务器：
sudo systemctl restart nfs-kernel-server


## 客户端
192.168.52.128
192.168.52.131

安装软件包
sudo apt-get update
sudo apt-get install nfs-common

在客户端上创建安装点
sudo mount 192.168.52.132:/home/python/share /home/python/dblog/media

测试NFS访问
touch /home/python/dblog/media/ckupload/general.test

开机自动挂载NFS共享目录: sudo vim /etc/fstab
192.168.52.132:/home/python/share/home/python/dblog/media nfs auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0
