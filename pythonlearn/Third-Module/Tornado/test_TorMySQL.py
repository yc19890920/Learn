from tornado.ioloop import IOLoop
from tornado import gen
import tormysql

pool = tormysql.helpers.ConnectionPool(
    max_connections = 20, #max open connections
    idle_seconds = 7200, #conntion idle timeout time, 0 is not timeout
    wait_connection_timeout = 3, #wait connection timeout
    host = "127.0.0.1",
    user = "root",
    passwd = "123456",
    db = "mysql",
    charset = "utf8"
)

@gen.coroutine
def test():
    tx = yield pool.begin()
    try:
        yield tx.execute("INSERT INTO test(id) VALUES(1)")
    except:
        yield tx.rollback()
    else:
        yield tx.commit()

    cursor = yield pool.execute("SELECT * FROM test")
    datas = cursor.fetchall()

    print datas

    yield pool.close()

ioloop = IOLoop.instance()
ioloop.run_sync(test)