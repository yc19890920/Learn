import tornado.httpserver as httpserver
import tornado.ioloop as ioloop
import tornado.options as options
import tornado.web as web
import asyncio
import uvloop
import asyncpg
import tornado_asyncio
import motor_asyncio

options.parse_command_line()

class IndexHandler(web.RequestHandler):
    def get(self):
        self.finish("It works")

class DatabaseHandler(web.RequestHandler):
    async def get(self):
        conn = await asyncpg.connect('postgresql://postgres@localhost/test')

        # rows = await conn.fetchrow('select pg_sleep(5)')
        rows = await conn.fetchrow('select * from public.user')
        print(rows[0])
        await conn.close()

        self.finish("ok")


class PoolHandler(web.RequestHandler):
    async def get(self):
        pool = self.application.pool
        async with pool.acquire() as connection:
            # Open a transaction.
            async with connection.transaction():
                # Run the query passing the request argument.
                rows = await connection.fetch("SELECT * FROM public.user ")
                # rows = await connection.fetch("SELECT pg_sleep(1) ")
                print(rows)

        self.finish("ok")


class App(web.Application):
    def __init__(self, pool):
        settings = {
            'debug': True
        }
        self._pool = pool
        super(App, self).__init__(
            handlers=[
                (r'/', IndexHandler),
                (r'/db', DatabaseHandler),
                (r'/pool', PoolHandler),
            ],
            **settings)

    @property
    def pool(self):
        return self._pool


async def init_db_pool():
    return await asyncpg.create_pool(database='test',
                                     user='postgres')


def init_app(pool):
    app = App(pool)
    return app


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    tornado_asyncio.AsyncIOMainLoop().install()

    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(init_db_pool())
    app = init_app(pool=pool)
    server = httpserver.HTTPServer(app, xheaders=True)
    server.listen(5040)
    loop.run_forever()