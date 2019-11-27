
## 启动supervisor
sudo /usr/bin/python /usr/bin/supervisord -c  ~/git/dblog/doc/supervisord.conf
sudo /usr/bin/python /usr/bin/supervisorctl -c  ~/git/dblog/doc/supervisord.conf


sudo /usr/bin/python /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
sudo /usr/bin/python /usr/bin/supervisorctl -c /etc/supervisor/supervisord.conf

### 开机启动 /etc/rc.local 加入如下代码
/usr/bin/python /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
/usr/bin/python /usr/bin/supervisorctl -c /etc/supervisor/supervisord.conf
或者
/usr/bin/python /usr/bin/supervisord -c /home/python/conf/supervisord.conf
/usr/bin/python /usr/bin/supervisorctl -c  /home/python/conf/supervisord.conf


# centos
修改 /etc/rc.d/rc.local 这个文件：
例如将 apache、mysql、samba、svn 等这些服务的开机自启动问题一起搞定：