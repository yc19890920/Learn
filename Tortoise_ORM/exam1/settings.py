import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = config('FASTAPI_DEBUG', default=False, cast=bool)
SECRET_KEY = config('API_SECRET', default='^=2p4poluvn4m(4_!wops2&$4*qth7qxgb-j@!4kuf6n%bs#2#')

PROJECT_CODE = 'REWARD'

DB_HOST = config('DB_HOST', default='192.168.1.24')
DB_PORT = config('DB_PORT', default=3306)
DB_USER = config('DB_USER', default='root')
DB_PASSWORD = config('DB_PASSWORD', default='123456')
DB_NAME = config('DB_NAME', default='tortoise')
DB_ECHO = config('DB_ECHO', default=True, cast=bool)

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': DB_HOST,
                'port': DB_PORT,
                'user': DB_USER,
                'password': DB_PASSWORD,
                'database': DB_NAME,
                'echo': DB_ECHO,
                "charset": "utf8mb4",
                "minsize": 1,
                "maxsize": 5,
            }
        },
    },
    'apps': {
        'models': {
            'models': ['app.models'],
            'default_connection': 'default',
        },
    },
}
REDIS_HOST = config('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = config('REDIS_PORT', default=6379)
REDIS_PASSWORD = config('REDIS_PASSWORD', default='')

REDIS = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'password': REDIS_PASSWORD,
    'db': 1,
    'encoding': 'utf-8'
}

ARQ = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'password': REDIS_PASSWORD,
    'database': 2,
}
