sudo yum install -y nginx
systemctl start nginx.service

## nginx  配置
- cd /etc/nginx/conf.d

### 配置
```
# the upstream component nginx needs to connect to

upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8080; # for a web port socket (we'll use this first)
}


# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    server_name  djangoblog.com;

   
        access_log          /home/python/log/nginx_djangoblog;
        error_log           /home/python/log/nginx_djangoblog_err;

        proxy_connect_timeout    600;
        proxy_read_timeout       600;
        proxy_send_timeout       600;

    # max upload size
        client_max_body_size 50M;

        location ^~ /static/ {
            # your own static file
            root /home/python/git/dblog/;
            if ($query_string) {
                expires max;
            }
            #expires 30d;
            #break;
        }
        
        location /media/ {
            root /home/python/git/dblog/;
            expires 30d;
            break;
        }

    # Django media
    #location /media  {
    #    alias /path/to/your/mysite/media;  # your Django project's media files - amend as required
    #}

    #location /static {
    #    alias /home/python/git/dblog/static/; # your Django project's static files - amend as required
    #}

    # Finally, send all non-media requests to the Django server.
        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://django;
        }


        #-- Error page setting ---------------------------
        error_page          404              /404.html;
        error_page          500 502 503 504  /50x.html;
        location = /50x.html {
                 root            /home/python/git/dblog/templates/errpage;
        }
        location = /404.html {
                 root            /home/python/git/dblog/templates/errpage;
        }
}
```

