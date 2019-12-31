FROM mylxsw/wizard:latest

# 数据库连接配置
# 这里可以根据需要添加其它的Env配置，可用选项参考项目的.env.example文件
ENV DB_CONNECTION=mysql
ENV DB_HOST=192.168.183.133
ENV DB_PORT=3306
ENV DB_DATABASE=wizard_2
ENV DB_USERNAME=wizard
ENV DB_PASSWORD=wizard
ENV WIZARD_NEED_ACTIVATE=false
# 访问地址，只有正确配置后，导出的 markdown 文档图片才能正常展示
ENV APP_URL=http://192.168.183.133:8080

# 文件上传存储目录
VOLUME /webroot/storage/app/public

RUN php artisan config:cache