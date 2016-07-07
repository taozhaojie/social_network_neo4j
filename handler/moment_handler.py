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
					uid = self.get_argument('me', 0)
					page = self.get_argument('page', 0)
					Moment.list(uid,page,self)

		else:
			if not action:
				self.render('moment.html')
			else:
				if action == 'v':
					Moment.list_one(self)
				elif action == 'like':
					uid = self.get_argument('me', 0)
					Moment.like(vid,uid,self)
				elif action == 'liked':
					Moment.liked(vid,self)
				elif action == 'reply':
					Moment.reply_get(vid,self)


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
					Moment.reply(vid,text,uid,self)