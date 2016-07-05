import route
from settings import setting

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path

port_id = 3000

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = setting
        
        tornado.web.Application.__init__(self, route.route, **settings)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	Application().listen(port_id)
	print '# server start at port', port_id
	tornado.ioloop.IOLoop.instance().start()
	