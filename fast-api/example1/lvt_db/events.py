import aiomysql
from fastapi import FastAPI

from lvt_core.logger import logger
from lvt.settings import MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT


async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to mysql")
    app.state.pool = await aiomysql.create_pool(
        host='192.168.1.24', port=3306,
        user='root', password='123456',
        db='mysql',
        loop=None, autocommit=False,
        min_size=MIN_CONNECTIONS_COUNT,
        max_size=MAX_CONNECTIONS_COUNT,
    )
    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")
    await app.state.pool.close()
    logger.info("Connection closed")
