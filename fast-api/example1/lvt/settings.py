import os
import sys
import logging
from typing import List
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Token"  # noqa: S105
VERSION = "0.0.0"

# config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

# DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default='^=2p4poluvn4m(4_!wops2&$4*qth7qxgb-j@!4kuf6n%bs#2#')
JWT_ALGORITHM: str = config("JWT_ALGORITHM", cast=str, default='HS256')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = config("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30)

PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI example application")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=""
)

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=LOGGING_LEVEL)
