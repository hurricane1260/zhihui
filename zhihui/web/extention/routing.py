# coding=utf-8

"""
    Usage:
    @route(r'/login', name='login')
    class Login(tornado.web.RequestHandler):
        ...

    class Application(tornado.web.Application):
        def __init__(self):
            handlers = [
                ...
            ] + Route.routes()
            ...
"""

from tornado.web import url


class Route(object):
    """
        Route
    """
    _routes = {}

    def __init__(self, pattern, kwargs={}, name=None, host='.*$'):
        """
            __init__
        """
        print "__init__"
        self.pattern = pattern
        self.kwargs = {}
        self.host = host
        self.name = name

    def __call__(self, handler_class):
        """
            __call__
        """
        spec = url(self.pattern, handler_class, self.kwargs, name=self.name)
        self._routes.setdefault(self.host, []).append(spec)
        return handler_class

    @classmethod
    def routes(cls):
        """
            routes
        """
        return reduce(lambda x, y: x+y, cls._routes.values()) if cls._routes else []

route = Route
