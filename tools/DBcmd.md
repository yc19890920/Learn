1. mysql数据库连接：
# emd_web   XnLaT34LxaQViNB
- mysql -h 192.168.50.51 -u edm_web -P 3306 -p
- mysql -h host -u user -P port -p
- mysql -h 127.0.0.1 -u root -p 123456 -P 3306

### 
- 创建数据库
CREATE DATABASE tornado_test DEFAULT CHARACTER SET UTF8;
CREATE schema tornado_test default character set utf8 collate utf8_general_ci;

- 创建用户
create user 'tornado'@'%' identified by 'tornado123';

- 授权 tornado 用户拥有 tornado_test 数据库的所有权限。
GRANT ALL ON tornado_test.* TO 'tornado'@'%';

- 部分授权
GRANT SELECT, INSERT ON tornado_test.* TO 'tornado'@'%';
GRANT ALL ON . TO 'tornado'@'%';

- 启用修改
flush  privileges;

- [MySQL创建用户与授权方法_Mysql](https://yq.aliyun.com/ziliao/134218)
- [MySQL创建数据库与创建用户以及授权](http://surenpi.com/2017/06/16/mysql_create_user_and_auth/)
- [mysql如何在命令行创建数据库](http://www.cnblogs.com/Just--Do--It/p/7944108.html)
- [MySQL添加用户、删除用户与授权](http://www.cnblogs.com/wanghuaijun/p/5802209.html)




### 
2. mongoDB 数据库连接：
- mongo -u user -p passwd  127.0.0.1/dbname
- mongo -u mm-mc -p PFBgatL4Vq63sEP  127.0.0.1/mm-mc


### 
3. redis
- redis-cli


### 
4. pgsql
- psql -h 127.0.0.1 -U username -d dbname  其中username为数据库用户名，dbname为要连接的数据库名，执行后提示输入密码
- psql -U user -d dbname
- \c dbname 切换数据库,相当于mysql的use dbname
- \l 列举数据库，相当于mysql的show databases
- \dt 列举表，相当于show tables
- \d tblname 查看表结构，相当于desc tblname,show columns from tbname
