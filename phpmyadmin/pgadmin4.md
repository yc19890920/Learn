## Docker快速部署pgadmin4服务


docker run -d --name phppgadmin_local -e PHP_PG_ADMIN_SERVER_HOST=192.168.1.24 -e PHP_PG_ADMIN_SERVER_PORT=5432 -p 0.0.0.0:82:80 dockage/phppgadmin:latest

docker pull dpage/pgadmin4

docker run -p 80:80 \
    -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" \
    -e "PGADMIN_DEFAULT_PASSWORD=123456" \
    -d dpage/pgadmin4
    
    
   