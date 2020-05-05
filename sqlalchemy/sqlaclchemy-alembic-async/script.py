from model.base import db


def get_db():
    try:
        connect = db.engine.acquire()
        yield connect
    finally:
        connect.close()
