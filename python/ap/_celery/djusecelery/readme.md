
- [Django Celery](http://ychzp.top/p/86/)

## 启动worker (切换到manage.py同级目录下执行)
/home/python/pyenv/versions/djcelery363/bin/celery -A djusecelery worker -l info -P eventlet

/home/python/pyenv/versions/djcelery363/bin/celery -A djusecelery worker -l info -P gevent -c 4

/home/python/pyenv/versions/djcelery363/bin/celery -A djusecelery worker -l info -P gevent -c 4 -Q task_number_one,task_number_two,task_number_three

/home/python/pyenv/versions/djcelery363/bin/celery -A djusecelery worker -l info -P gevent -Q task_number_one,task_number_two,task_number_three

/home/python/pyenv/versions/djcelery363/bin/celery -A djusecelery worker -l info -P gevent -c 200 -Q task_number_one,task_number_two,task_number_three -n worker1.%h

/home/python/pyenv/versions/djcelery363/bin/celery -A djusecelery worker -l info -c 200 -Q task_number_one,task_number_two,task_number_three

/home/python/pyenv/versions/djcelery363/bin/celery -A djusecelery worker -l info -P gevent -c 50 -n worker1.%h -Q task_number_one,task_number_two,task_number_three,default-celery 

# 启动定时任务或周期性任务
/home/python/pyenv/versions/djcelery363/bin/celery -A djusecelery beat -l info


/home/python/pyenv/versions/djcelery363/bin/python manage.py makemigrations

/home/python/pyenv/versions/djcelery363/bin/python manage.py migrate

/home/python/pyenv/versions/djcelery363/bin/python manage.py createsuperuser

admin/1qaz@WSX

/home/python/pyenv/versions/djcelery363/bin/python manage.py runserver 0.0.0.0:6666


beat 启动的任务:
{
    'body': 'W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=',
    'content-encoding': 'utf-8',
    'content-type': 'application/json', 
    'headers': {
        'lang': 'py',
         'task': 'app.blog.tasks.task_number_three',
         'id': '58e78d7f-a683-4830-86d5-8fecbf4c531e',
         'shadow': None, 
         'eta': None, 
         'expires': None,
         'group': None,
         'retries': 0, 
         'timelimit': [None, None], 
         'root_id': '58e78d7f-a683-4830-86d5-8fecbf4c531e', 
         'parent_id': None, 
         'argsrepr': '()', 
         'kwargsrepr': '{}', 
         'origin': 'gen14321@python-virtual-machine'
    }, 
    'properties': {
        'correlation_id': '58e78d7f-a683-4830-86d5-8fecbf4c531e', 
        'reply_to': 'f5bb8663-b446-3252-9454-879a0de641cd', 
        'delivery_mode': 2, 
        'delivery_info': {
            'exchange': '', 
            'routing_key': 'task_number_three'
        }, 
        'priority': 0, 
        'body_encoding': 'base64', 
        'delivery_tag': '692d4952-0e5a-4f9e-9666-b464b9fd36fb'
    }
}