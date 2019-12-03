docker run -d \
        --name phphmyadmin_local_tidb \
        -e PMA_HOST=192.168.1.24 \
        -e PMA_PORT=4000 \
        -p 8070:80 \
        phpmyadmin/phpmyadmin
