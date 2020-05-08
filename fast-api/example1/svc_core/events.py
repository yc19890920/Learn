from typing import Callable
from fastapi import FastAPI

from svc_core.logger import logger
from svc_db.events import close_db_connection, connect_to_db


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        print("connect_to_db(app)")
        # await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        print("close_db_connection(app)")
        # await close_db_connection(app)

    return stop_app
