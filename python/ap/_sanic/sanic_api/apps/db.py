from peewee import MySQLDatabase
from . import settings

db = MySQLDatabase('sanic_test', **settings.MYSQL_DATABASES['sanic'])