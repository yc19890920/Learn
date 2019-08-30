异步任务

启动 Celery Worker 进程，在项目的根目录下执行下面命令：
demo $ celery -A celeryApp worker --loglevel=info

接着，运行 $ python client.py，它会发送两个异步任务到 Broker，在 Worker 的窗口我们可以看到如下输出：

指定多个队列：
celery -A celeryApp worker --loglevel=info --queues test_celey_queue_add,test_celey_queue_multiply

celery -A celeryApp worker --loglevel=info --Q test_celey_queue_add,test_celey_queue_multiply -f /data/test.celery/celery.log



一旦使用了 scheduler, 启动 celery需要加上-B 参数
celery -A celeryApp worker -B --loglevel=info
celery -A celeryApp worker -B -l info
