

- [搭建Tornado+Nginx](http://www.cnblogs.com/ArtsCrafts/p/3646268.html)
- [ubuntu+nginx+supervisor部署tornado](http://ningning.today/2015/10/04/python/ubuntu-nginx-supervisor%E9%83%A8%E7%BD%B2tornado/)
- [Ubuntu14.04下搭建配置nginx与Tornado反向代理](http://lambda.hk/nginx/2015/04/30/nginx-tornado/)
- [第八章：部署Tornado](http://demo.pythoner.com/itt2zh/ch8.html)
- [CentOS使用Nginx+Tornado+Supervisor搭建Python web服务](http://luokr.com/p/2)
- [tornado 概览](http://www.tornadoweb.cn/documentation)


###
systemctl restart nginx.service

- /etc/nginx/conf.d/tornado.conf
```
upstream tornado {
        server 127.0.0.1:8000;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
        server 127.0.0.1:8003;
    }


# Only retry if there was a communication error, not a timeout
# on the Tornado server (to avoid propagating "queries of death"
# to all frontends)

server {
        listen 80;
        server_name  torlearn.cn

        access_log /var/log/nginx/tornado_log;
        error_log /var/log/nginx/tornado_error;

        proxy_connect_timeout    600;
        proxy_read_timeout       600;
        proxy_send_timeout       600;

        # Allow file uploads
        client_max_body_size 50M;

        location ^~ /static/ {
            # your own static file
            root /home/python/git_worker/python_learn/Third-Module/Tornado/web/;
            if ($query_string) {
                expires max;
            }
            #expires 30d;
            #break;
        }

        # ---- TEST -----
        # --------------

        #location = /favicon.ico {
        #    rewrite (.*) /static/favicon.ico;
        #}

        #location = /robots.txt {
        #    rewrite (.*) /static/robots.txt;
        #}

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://tornado;
        }

        #-- Error page setting ---------------------------
        error_page          404              /404.html;
        error_page          500 502 503 504  /50x.html;
        location = /50x.html {
                 root            /home/python/git_worker/python_learn/Third-Module/Tornado/web/errpage;
        }
        location = /404.html {
                 root            /home/python/git_worker/python_learn/Third-Module/Tornado/web/errpage;
        }
}
```