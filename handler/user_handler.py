import tornado.web
from model.user import User
from tornado.escape import json_encode

class UserHandler(tornado.web.RequestHandler):

	# @tornado.web.asynchronous
	def get(self, vid):
		action = self.get_argument('action', 0)

		if not vid:
			if not action:
				self.render('user.html')
			else:
				if action == 'v': #view
					Moment.list(self)
		else:
			if vid == 'friend':
				uid = self.get_argument('me', 0)
				if action == 'req':
					User.friend_query(uid, self)
				elif action == 'v':
					User.friend_list(uid, self)

			else:
				if not action:
					self.render('user.html')
				else:
					pass

	# @tornado.web.asynchronous
	def post(self, vid):
		action = self.get_argument('action', 0)

		if not vid:
			pass

		else:
			if vid == 'friend':
				if not action:
					pass
				else:
					init_user = self.get_argument('init_user', 0)
					recv_user = self.get_argument('recv_user', 0)

					if action == 'req': # friendship request
						User.friend_request(init_user, recv_user, self)
					elif action == 'ack':
						User.friend_accept(init_user, recv_user, self)
					elif action == 'del':
						User.friend_delete(init_user, recv_user, self)
