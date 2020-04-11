#!/usr/bin/env bash

# All static files is hosted inside the cluster, refer to: deploy/k8s.yaml
export DJANGO_SECRET_KEY='^=2p4poluvn4m(4_!wops2&$4*qth7qxgb-j@!4kuf6n%bs#2#'
export DJANGO_DEBUG='1'
export DB_DFT_ENGINE='django.db.backends.mysql'
export DB_DFT_USERNAME='root'
export DB_DFT_PASSWORD='123456'
export DB_DFT_DATABASE='dblog'
export DB_DFT_HOSTNAME='192.168.1.24'
export DB_DFT_PORT=3306
export DJANGO_CACHE_REDIS='redis://192.168.1.24:6379'
export DJANGO_ALLOWED_HOSTS='* 192.168.1.24 127.0.0.1'


#if [ -f /etc/secrets/storage/sa/credentials.json ]; then
#    export GOOGLE_APPLICATION_CREDENTIALS=/etc/secrets/storage/sa/credentials.json
#fi

if [ "$1" = 'shell' ]; then
    python manage.py shell
    exit 0
elif [ "$1" = 'dbshell' ]; then
    python manage.py dbshell
    exit 0
elif [ "$1" = 'createsuperuser' ]; then
    python manage.py createsuperuser
    exit 0
elif [ "$1" = 'init-mysql' ]; then
    echo "Running $1"
    python manage.py migrate
    exit 0
elif [ "$1" = 'report' ]; then
    echo "Running report"
    python3 report.py
    exit 0
fi

# Collect static files to STATIC_ROOT
# python manage.py collectstatic --clear --noinput

exec gunicorn \
    --workers 4 \
    --pid /var/run/gunicorn.pid \
    --bind 0.0.0.0:8000 \
    --worker-class=egg:meinheld#gunicorn_worker \
    --worker-connections=2000 \
    --backlog=2048 \
    --keep-alive 5 \
    --limit-request-line 16384 \
    --limit-request-field_size 16384 \
    --timeout 300 \
    --log-level=info \
    --access-logfile=- \
    --error-logfile=- \
    --access-logformat='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
    "dblog.wsgi:application"