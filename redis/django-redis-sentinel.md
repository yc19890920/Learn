- [Plugin for django-redis that supports Redis Sentinel](https://github.com/SpatialBuzz/django-redis-sentinel)
- [Django-Redis Client that supports Sentinel Cluster HA](https://github.com/danigosa/django-redis-sentinel-redux)
- [celery-redis-sentinel](https://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html)

pip install django-redis-sentinel
```
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis_master/sentinel-host1:2639,sentinel-host2:2639/0"
            "OPTIONS": {
                "PASSWORD": 's3cret_passw0rd!',
                "CLIENT_CLASS": "django_redis_sentinel.SentinelClient",
            }
        }
    }
    
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://127.0.0.1:6379?db=1",
            "redis://127.0.0.1:6379?db=1",
        ],
        "OPTIONS": {
            # "PASSWORD": 's3cret_passw0rd!',
            "CLIENT_CLASS": "django_redis_sentinel.SentinelClient",
        }
    },
}
```

These are top-level settings in settings.py
DJANGO_REDIS_CLOSE_CONNECTION - Close connection after each request, off will allow persistant connections (default False)


celery-redis:
```
# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ["json"]            # 指定任务接受的内容类型.
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TASK_RESULT_EXPIRES = 60 * 5 * 1   # 指定任务过期时间 1小时
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_DEFAULT_QUEUE =  'linux-webvue-celery-default' # 	默认队列
CELERYD_MAX_TASKS_PER_CHILD = 50    # 每个worker最多执行50个任务就会被销毁，可防止内存泄露 # 每个worker执行了多少任务就会死掉，默认是无限的
CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁
CELERYD_PREFETCH_MULTIPLIER = 1  # celery worker 每次去rabbitmq预取任务的数量
```

celery-sentinel:
```
app.conf.broker_url = 'sentinel://localhost:26379;sentinel://localhost:26380;sentinel://localhost:26381'
app.conf.broker_transport_options = { 'master_name': "cluster1" }

app.conf.broker_transport_options = {'visibility_timeout': 3600}  # 1 hour.
app.conf.result_backend_transport_options = {'master_name': "mymaster"}
```

