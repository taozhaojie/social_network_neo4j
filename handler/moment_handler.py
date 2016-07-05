import tornado.web
from model.moment import Moment
from tornado.escape import json_encode

class MomentHandler(tornado.web.RequestHandler):
	# @tornado.web.asynchronous
	def get(self, vid):
		action = self.get_argument('action', 0)

		if not vid:
			if not action:
				self.render('moment.html')
			else:
				if action == 'v': #view
					Moment.list(self)
		else:
			if not action:
				self.render('moment.html')
			else:
				if action == 'v':
					Moment.list_one(self)

	# @tornado.web.asynchronous
	def post(self, vid):

		text = self.get_argument('text', '')
		uid = self.get_argument('uid', '')

		if not text:
			ret = {'ret': 1, 'err': 'no text content'}
			self.write(json_encode(ret))

		else:
			if not uid:
				ret = {'ret': 1, 'err': 'no uid provided'}
				self.write(json_encode(ret))

			else:
				if not vid:
					Moment.create(text,uid,self)

				else:
					Moment.reply(self)