# -*- coding: utf-8 -*-

import tornado
import tornadoredis
from config import *
from tornado import web, gen
from tornado.options import options


class BaseHandler(web.RequestHandler):

    def get_login_url(self):
        return u"/login"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None



class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.html", next=self.get_argument("next", "/"))

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        # The authenticate method should match a username and password
        # to a username and password hash in the database users table.
        # Implementation left as an exercise for the reader.
        # auth = self.db.authenticate(username, password)
        if username == options.USERNAME and password == options.PASSWORD:
            auth = True
        else:
            auth = False
        if auth:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", u"/"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect.")
            self.redirect(u"/login" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/login")

class MainHandler(BaseHandler):

    # @tornado.web.authenticated
    def get(self):
        # self.redirect(u"/report")
        self.render('index.html')

def main():
    app = tornado.web.Application(
        [
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/", MainHandler),
        ],

        CONNECTION_POOL=tornadoredis.ConnectionPool(host=options['REDIS_DB_HOST'], port=options['REDIS_DB_PORT'],
                                                    max_connections=100, wait_for_available=True),
        cookie_secret="$1$uDOOIHw4$112sF6/JLaN6FYyAy6DmQ0",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        debug=True)

    # app.sentry_client = AsyncSentryClient(
    #     'http://1e04189a9e504d8cb6b124b9224dc50c:d150ce32dc764fb0bffe3b7569e0429c@202.103.191.86:9000/2'
    # )

    app.listen(options.PORT, options.WEB_SERVER_IP)
    ioloop = tornado.ioloop.IOLoop.instance()

    ioloop.start()


if __name__ == "__main__":
    main()
