ab压力测试的参数：

-c 500 并发数
-n 1000 请求数
还有更多的参数指令 请执行ab --help 查看，我们这里只用 c 和 n 
现在我们执行下高并发请求：
ab -c500 -n1000 http://106.12.212.131/msa/index1.php

This is ApacheBench, Version 2.3 <$Revision: 1430300 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 106.12.212.131 (be patient)
Completed 100 requests
......
然后我们在查看数据信息会有什么变化


执行下高并发请求：
curl http://127.0.0.1:10086/i
ab -c500 -n1000 http://127.0.0.1:10086/i1
数据如下：
id  num  version
1   -37 	 0




curl http://127.0.0.1:10086/i
ab -c500 -n1000 http://127.0.0.1:10086/i2


