
siege -c 200 -r 100 http://www.ycedm.com/login

Transactions(完成次数)
Availability(可用性)
Elapsed time(总共使用时长)
Data transferred(数据传输)
Response time(响应时间，显示网络连接的速度)
Transaction rate(平均每秒完成的处理次数)
Throughput(平均每秒传送数据)
Concurrency(实际最高并发连接数)
Successful transactions(成功处理次数)
Failed transactions(失败处理次数)
Longest transaction(最长传输时长)
Shortest transaction(最短传输时长)



ab -n 1000 -c 1000 http://www.ycedm.com/login


webbench -c 500 -t 60 http://www.ycedm.com/login

500个并发，在60秒内，请求成功344267个，失败数0个

