
- [Gunicorn settings](http://docs.gunicorn.org/en/stable/settings.html)
- [Gunicorn配置部分的翻译](https://www.cnblogs.com/nanrou/p/7026789.html)


/home/python/pyenv/versions/flask-blog/bin/gunicorn -c conf.py manage:app
# /home/python/pyenv/versions/flask-blog/bin/gunicorn -c configm.py manage:app


home/python/pyenv/versions/flask-blog/bin/gunicorn -w 16
    -b 127.0.0.1:8080
    django_app.wsgi:application
    --worker-class=egg:meinheld#gunicorn_worker
    --threads=30
    --worker-connections=2000
    --backlog=2048
    --access-logfile=/home/log/httpd/gun.log
    --error-logfile=/home/log/httpd/gun.error
    --user=apache --group=apache

/usr/local/pyenv/versions/edm_web/bin/gunicorn -c conf.py django_app.wsgi:application