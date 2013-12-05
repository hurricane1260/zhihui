# coding=utf-8

"""
    app
"""
import os
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options, define

define("port", default=8080, type=int, help="run on the given port")

try:
    import zhihui
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__),".."))


class Application(tornado.web.Application):
    """
    Application
    """
    def __init__(self):
        handlers = []
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            autoescape=None,
            debug=True,
            ui_modules=uimodules
        )
        tornado.web.Application.__init__(self, handlers=handlers, **settings)


def main():
    """
    main
    """
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()