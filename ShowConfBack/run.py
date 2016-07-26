from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from restful import app

import config

http_server = HTTPServer(WSGIContainer(app))

http_server.listen(config.server['port'], address=config.server['host'])
IOLoop.instance().start()