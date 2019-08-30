from celery.utils.log import get_task_logger, get_logger, get_multiprocessing_logger, task_logger
from celery import shared_task, task
from celery.schedules import crontab
import time
log = get_task_logger(__name__)

# 自定义要执行的task任务
@task(ignore_result=True, store_errors_even_if_ignored=True, priority=1)
def task_number_one():
    # log.info('......................................................hello celery and django...1')
    # time.sleep(3)
    # log.info('......................................................hello celery and django...2')
    return 1

@task(ignore_result=True, store_errors_even_if_ignored=True, priority=2)
def task_number_two():
    # time.sleep(2)
    return 2

# @task(ignore_result=True, store_errors_even_if_ignored=True, max_retries=10, throws=(AssertionError, ))
@task(ignore_result=True, store_errors_even_if_ignored=True, default_retry_delay=300, max_retries=5, priority=1)
# @task(ignore_result=True, store_errors_even_if_ignored=True, priority=1)
def task_number_three():
    # assert 1==2
    # log.info('......................................................task_number_three...1')
    # time.sleep(1)
    # log.info('......................................................task_number_three...2')
    # 再接异步队列
    task_number_two.delay()
    task_number_one.delay()
    return 3




from app.blog.models import Blog
from django.db import connection, connections

@task(ignore_result=True, store_errors_even_if_ignored=True, priority=1)
def excute_django_model():
    if not Blog.objects.exists():
        Blog.objects.create(title="title")
    return Blog.objects.first()


@task(ignore_result=True, store_errors_even_if_ignored=True, priority=1)
def excute_django_connection():
    sql = "select * from blog limit 1;"
    cr = connections['default'].cursor()
    # cr = connection.cursor()
    cr.execute(sql, ())
    # cr.fetchall()
    res= cr.fetchone()
    return res


    return Blog.objects.first()