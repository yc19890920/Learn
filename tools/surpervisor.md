

- [Supervisor官方文档](http://supervisord.org/)



### /etc/rc.local 加入如下代码
/usr/bin/python /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
/usr/bin/python /usr/bin/supervisorctl -c /etc/supervisor/supervisord.conf
或者
/usr/bin/python /usr/bin/supervisord -c /home/python/conf/supervisord.conf
/usr/bin/python /usr/bin/supervisorctl -c  /home/python/conf/supervisord.conf


# centos
修改 /etc/rc.d/rc.local 这个文件：
例如将 apache、mysql、samba、svn 等这些服务的开机自启动问题一起搞定：



[progran:example]              ;项目名
command=/bin/echo              ;supervisor启动时将要开启的进程。相对或绝对路径均可。若是相对路径则会从supervisord的$PATH变中查找。命令可带参数。  
priority=999                   ;指明进程启动和关闭的顺序。低优先级表明进程启动时较先启动关闭时较后关闭。高优先级表明进程启动时启动时较后启动关闭时较先关闭。  
autostart=true                 ;是否随supervisord启动而启动  
autorestart=true               ;进程意外退出后是否自动重启  
startsecs=10                   ;进程持续运行多久才认为是启动成功  
startretries=3                 ;重启失败的连续重试次数  
exitcodes=0,2                  ;若autostart设置为unexpected且监控的进程并非因为supervisord停止而退出，那么如果进程的退出码不在exitcode列表中supervisord将重启进程  
stopsignal=QUIT                ;杀进程的信号  
stopwaitsecs=10                ;向进程发出stopsignal后等待OS向supervisord返回SIGCHILD 的时间。若超时则supervisord将使用SIGKILL杀进程 