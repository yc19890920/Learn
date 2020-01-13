- [Ubuntu下MySQL主从同步配置步骤](https://www.linuxidc.com/Linux/2018-08/153588.htm)
- [MySQL设置只读模式](https://www.cnblogs.com/xiewenming/p/7590335.html)

## 首先设置一个 opene 用户可以访问 test 数据库
建议先不要设置 read_only = on， 等容器启动起来之后再运行：
set global read_only=1; 
```
CREATE DATABASE test DEFAULT CHARACTER SET UTF8;
create user 'opene'@'%' identified by '123456';
GRANT ALL ON test.* TO 'opene'@'%';
flush  privileges;
```

Ubuntu中安装一台mysql了，docker安装另外一台mysql
获取mysql的镜像，主从同步尽量保证多台mysql的版本相同，\我的ubuntu中存在的mysql是5.7.28版本，所以获取5.7.28版本的镜像为例：

docker image pull mysql:5.7.28

运行mysql docker镜像，需要在宿主机中建立文件目录用于mysql容器保存数据和读取配置文件。
在家目录中（/home/Python）中创建目录，将mysql的配置文件放到此目录中

cd ~
mkdir mysql_slave
cd mysql_slave
mkdir data
mkdir mysql.conf.d
cp /etc/mysql/mysql.conf.d/* ./mysql.conf.d/


将docker运行的mysql作为slave来运行，开启前需要修改配置文件。

编辑 ~/mysql_slave/mysql.conf.d/mysqld.cnf 文件，修改
port  =  6033
general_log  = 0
server-id  = 2

设置只读：
read_only = on
\#super_read_only = on
\#tx_read_only = on

让此台mysql运行在8306端口上，且mysql编号为2

创建docker容器
docker run --name mysql-slave -e MYSQL_ROOT_PASSWORD=123456 -d \
    --network=host \
    -v /home/python/Learn/django_serializers/mysql_ms/mysql_slave/data:/var/lib/mysql \
    -v /home/python/Learn/django_serializers/mysql_ms/mysql_slave/mysql.conf.d:/etc/mysql/mysql.conf.d  mysql:5.7.28
    
MYSQL_ROOT_PASSWORD 是创建mysql root用户的密码
测试，在ubuntu中使用mysql命令尝试连接docker容器中的mysql
mysql -uroot -p -h 127.0.0.1 -P 6033

## 2）备份主服务器原有数据到从服务器
如果在设置主从同步前，主服务器上已有大量数据，可以使用mysqldump进行数据备份并还原到从服务器以实现数据的复制。
在主服务器Ubuntu上进行备份，执行命令：
mysqldump -uroot -p123456 --all-databases --lock-all-tables > ~/master_db.sql

-u ：用户名
-p ：示密码
--all-databases ：导出所有数据库
--lock-all-tables ：执行操作时锁住所有表，防止操作时有数据修改
~/master_db.sql :导出的备份数据（sql文件）位置，可自己指定

在docker容器中导入数据
mysql -uroot -p -h127.0.0.1 --port=6033 < ~/master_db.sql
mysql -uroot -p123456 -h127.0.0.1 --port=6033 < ~/master_db.sql

## 3）配置主服务器master（Ubuntu中的MySQL）
编辑设置mysqld的配置文件，设置log_bin和server-id
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf

server-id		= 1
log_bin			= /var/log/mysql/mysql-bin.log


重启mysql服务
sudo service mysql restart

登入主服务器Ubuntu中的mysql，创建用于从服务器同步数据使用的帐号
mysql -uroot -p -h 127.0.0.1 -P 3306
GRANT REPLICATION SLAVE ON *.* TO 'slave'@'%' identified by 'slave';
FLUSH PRIVILEGES;

获取主服务器的二进制日志信息
SHOW MASTER STATUS;

File为使用的日志文件名字，Position为使用的文件位置，这两个参数须记下，配置从服务器时会用到。

## 4）配置从服务器slave （docker中的mysql）
进入docker中的mysql
mysql -uroot -p123456 -h 127.0.0.1 --port=6033
执行
change master to master_host='127.0.0.1', master_user='slave', master_password='slave',master_log_file='mysql-bin.000002', master_log_pos=10925;

master_host：主服务器Ubuntu的ip地址
master_log_file: 前面查询到的主服务器日志文件名
master_log_pos: 前面查询到的主服务器日志文件位置
启动slave服务器，并查看同步状态

start slave;
show slave status \G


将slave数据库read-only=1设置只读后，在master执行
GRANT USAGE ON *.* TO 'test'@'localhost' IDENTIFIED BY'123456' WITH GRANT OPTION;
（这里要区别上面给从库分配复制权限的写法，这里分配的是usage权限， 后面多了with grant option）
创建一个普通用户，
然后用普通用户登录从库，执行操作会报错。切换到root用户后还是可以进行增删改查的。

GRANT USAGE ON *.* TO 'test'@'localhost' IDENTIFIED BY'123456' WITH GRANT OPTION;
