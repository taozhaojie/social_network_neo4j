import tornado.web

class UserHandler(tornado.web.RequestHandler):
	def get(self, vid):
		self.render('user.html')