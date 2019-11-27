152.168.52.129
152.168.52.130

虚拟IP: 192.168.52.133

sudo apt-get update
sudo apt-get install nginx keepalived
sudo apt-get install libpcre3-dev zlibc zlib-bin zlib1g-dev


# Nginx 配置
```
upstream default_pools{
    # 定义负载均衡组为default_pools,可以同时定义多个
    # server 192.168.52.128;
    # server 192.168.52.131;
	server 192.168.52.128:80 weight=2 max_fails=3 fail_timeout=20s;
	server 192.168.52.131:80 weight=1 max_fails=3 fail_timeout=20s;
} 
upstream static_pools {
	   server 192.168.52.128:80;
}
upstream media_pools {
	   server 192.168.52.131:80;
}
server {
    listen      80;
    # server_name  192.168.52.133;
    server_name  djangoweb.com www.djangoweb.com;

    access_log          /home/python/dblog_nginx.log;
    error_log           /home/python/dblog_nginx_erorr.log;

    proxy_connect_timeout    600;
    proxy_read_timeout       600;
    proxy_send_timeout       600;

    # max upload size
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://default_pools;
        proxy_set_header Host  $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
    
    # location /static/ {
    #    proxy_pass http://static_pools;
    #    proxy_set_header Host  $host;
    #    proxy_set_header X-Forwarded-For $remote_addr;
    #}
    
    #location /media/ {
    #    proxy_pass http://media_pools;
    #    proxy_set_header Host  $host;
    #    proxy_set_header X-Forwarded-For $remote_addr;
    #}
}
```

```
    location /static/ {
        proxy_pass http://static_pools;
        proxy_set_header Host  $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
    
    location /media/ {
        proxy_pass http://media_pools;
        proxy_set_header Host  $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
```


## 配置两台前端服务器的keepalived
增加虚拟IP:
主机（152.168.52.129）上增加：
sudo ifconfig  ens33:0 192.168.52.133 netmask 255.255.255.0
删除虚拟IP: ip addr del 192.168.52.133 dev ens33

sudo vim /etc/keepalived/check_nginx.sh

sudo chmod u+x /etc/keepalived/check_nginx.sh

```
#!/bin/bash  
A=`ps -C nginx --no-header |wc -l`  
if [ $A -eq 0 ];then  
 /etc/init.d/nginx start  
sleep 3  
if [ `ps -C nginx --no-header |wc -l`-eq 0 ];then  
 /etc/init.d/keepalived stop
fi  
fi
```

sudo vim /etc/keepalived/keepalived.conf #keepalived.conf 默认是没有的

这里说一下 keepalived 配置在两台 nginx节点上的区别：
    state 不同，MASTER 和 BACKUP
    priority 不同，MASTER 要高于 BACKUP
    mcast_src_ip  各自nginx服务器的实际IP
    
```
vrrp_script check_nginx {
	script "/etc/keepalived/check_nginx.sh"
	interval 2
	weight 2
}

global_defs {
	notification_email {
		
	}
}
vrrp_instance VI_1 {
	state MASTER
	interface ens33
	virtual_router_id 51 
	mcast_src_ip 152.168.52.129
	priority 20
	advert_int 1
	
	authentication {
		auth_type PASS
		auth_pass 123456
	}
	track_script {
		check_nginx
	}
	virtual_ipaddress {
		192.168.52.133
	}
}
```

152.168.52.130上面：
```
vrrp_script check_nginx {
	script "/etc/keepalived/check_nginx.sh"
	interval 2
	weight 2
}

global_defs {
	notification_email {
		
	}
}
vrrp_instance VI_1 {
	state BACKUP
	interface ens33
	virtual_router_id 51 
	mcast_src_ip 152.168.52.130
	priority 18
	advert_int 1
	
	authentication {
		auth_type PASS
		auth_pass 123456
	}
	track_script {
		check_nginx
	}
	virtual_ipaddress {
		192.168.52.133
	}
}
```
sudo service nginx reload
sudo service keepalived reload
sudo service nginx restart
sudo service keepalived restart 

systemctl restart nginx.service keepalived.service 