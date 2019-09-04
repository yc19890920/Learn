# -*- coding:utf-8 -*-

# 导入pysnowflake客户端
import snowflake.client as cli

# 链接服务端并初始化一个pysnowflake客户端
host = '192.168.1.24'
port = 30001
cli.setup(host, port)


# 生成一个全局唯一的ID（在MySQL中可以用BIGINT UNSIGNED对应）
guid = cli.get_guid()
print guid
# 4266484383127441409
# 4266484419357839361

# 查看当前状态
stats = cli.get_stats()
print stats
