
- [snowflake 分布式唯一ID生成器](https://www.cnblogs.com/galengao/p/5780519.html)
- [Welcome to Python SnowFlake’s documentation!](https://pysnowflake.readthedocs.io/en/latest/)
- [面试之支撑日活百万用户的高并发系统，应该如何设计其数据库架构](https://www.javazhiyin.com/39353.html)

pip install pysnowflake

启动pysnowflake服务

snowflake_start_server \
  --address=192.168.10.145 \
  --port=30001 \
  --dc=1 \
  --worker=1 \
  --log_file_prefix=/tmp/pysnowflask.log \
  --debug
  
snowflake_start_server \
  --address=0.0.0.0 \
  --port=30001 \
  --dc=1 \
  --worker=1 \
  --log_file_prefix=/tmp/pysnowflask.log \
  --debug
  
# --address：本机的IP地址默认localhost这里解释一下参数意思（可以通过--help来获取）：
# --dc：数据中心唯一标识符默认为0
# --worker：工作者唯一标识符默认为0
# --log_file_prefix：日志文件所在位置
  
  
