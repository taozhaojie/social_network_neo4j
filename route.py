from handler.index_handler import IndexHandler
from handler.user_handler import UserHandler
from handler.moment_handler import MomentHandler

route = [
    (r'/', IndexHandler),
    (r'/user/?(\w+)?', UserHandler),
    (r'/moment/?(\w+)?', MomentHandler),
]