import tornado.httpserver as httpserver
import tornado.ioloop as ioloop
import tornado.options as options
import tornado.web as web
import asyncio
import uvloop
from motor import motor_asyncio
from tornado import tornado_asyncio

options.parse_command_line()

class IndexHandler(web.RequestHandler):
    def get(self):
        self.finish("It works")

class MongodbHandler(web.RequestHandler):
    async def get(self):
        ret = await self.application.motor_client.hello.find_one()
        # ret = await self.application.motor_client.hello.insert({'hello': 'world'})
        print(ret)
        self.finish("It works !")

class App(web.Application):
    def __init__(self):
        settings = {
            'debug': True
        }
        super(App, self).__init__(
            handlers=[
                (r'/', IndexHandler),
                (r'/mongodb', MongodbHandler),

            ],
            **settings)

    @property
    def motor_client(self):
        # client = motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
        client = motor_asyncio.AsyncIOMotorClient('mongodb://mm-mc:PFBgatL4Vq63sEP@127.0.0.1:27017/mm-mc')
        return client['test']


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    tornado_asyncio.AsyncIOMainLoop().install()
    app = App()
    server = httpserver.HTTPServer(app, xheaders=True)
    server.listen(5060)
    asyncio.get_event_loop().run_forever()
