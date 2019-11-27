#!/usr/bin/env bash

#if [ "$DATABASE" = "mysql" ]
#then
#    echo "Waiting for mysql..."
#
#    while ! nc -z $SQL_HOST $SQL_PORT; do
#      sleep 0.1
#    done
#
#    echo "mysql started"
#fi
mkdir -p /usr/src/app/log
mkdir -p /var/log/supervisor
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
# python manage.py collectstatic --no-input --clear

exec "$@"