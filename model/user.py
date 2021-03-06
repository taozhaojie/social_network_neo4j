import db
import function
from tornado import gen
from tornado.escape import json_encode

class User(object):
	def __init__(self,vid,action):
		self.vid = vid
		self.action = action

	@classmethod
	def list(self,sf):
		sf.write('123')

	@classmethod
	def friend_request(self,init_user,recv_user,sf):
		init_user = str(init_user)
		recv_user = str(recv_user)

		cql = '''
				MATCH (usr1:User {uid:%s})-[r:FRIEND_REQ]-(usr2:User {uid:%s})
				RETURN count(r)'''%(init_user, recv_user)
		res = db.cypher.execute(cql)
		if int(res[0][0]) > 0:
			ret = {'ret': 1, 'err': 'already requested'}
			sf.write(json_encode(ret))
			print ret

		else:
			cql = '''
					MATCH (usr1:User {uid:%s}), (usr2:User {uid:%s})
					CREATE (usr1)-[:FRIEND_REQ {timestamp: %i}]->(usr2)'''%(init_user, recv_user, function.timestamp())
			res = db.cypher.execute(cql)
			print '#', res

	@classmethod
	def friend_query(self,uid,sf):
		uid = str(uid)
		cql = '''
				MATCH (me)
				WHERE me.uid=%s
				OPTIONAL MATCH (me)<-[r:FRIEND_REQ]-(init_user)
				RETURN init_user'''%uid
		res = db.cypher.execute(cql)

		ret = []
		try:
			for usr in res:
				ret.append(usr[0].properties)
		except:
			pass

		sf.write(json_encode({'ret':0, 'data':ret}))

	@classmethod
	def friend_accept(self,init_user,recv_user,sf):
		init_user = str(init_user)
		recv_user = str(recv_user)

		cql = '''
				MATCH (usr1:User {uid:%s})-[r:FRIEND_REQ]->(usr2:User {uid:%s}) 
				DELETE r 
				WITH usr1,usr2 
				CREATE (usr1)-[:FRIEND {timestamp:%i}]->(usr2)'''%(init_user, recv_user, function.timestamp())
		res = db.cypher.execute(cql)
		print '#', res

	@classmethod
	def friend_list(self,uid,sf):
		uid = str(uid)
		cql = '''
				MATCH (me)
				WHERE me.uid=%s
				OPTIONAL MATCH (me)-[r:FRIEND]-(friend)
				RETURN friend'''%uid
		res = db.cypher.execute(cql)

		ret = []
		try:
			for usr in res:
				ret.append(usr[0].properties)
		except:
			pass

		sf.write(json_encode({'ret':0, 'data':ret}))

	@classmethod
	def friend_delete(self,init_user,recv_user,sf):
		init_user = str(init_user)
		recv_user = str(recv_user)

		cql = '''
				MATCH (usr1:User {uid:%s})-[r:FRIEND]->(usr2:User {uid:%s}) 
				DELETE r'''%(init_user,recv_user)
		res = db.cypher.execute(cql)

		sf.write(json_encode({'ret':0}))

	@classmethod
	def get_notification(self,vid,sf):
		vid = str(vid)
		cql = '''
				MATCH (me)
				WHERE me.uid=%s
				MATCH (me)-[:SUBS_FROM]-(subs)-[:SUBS_TO]-(target)-[:NEXT*0..]-(posts)-[:POST]-(owner)
				WITH subs, target, owner
				MATCH (subs)-[:NOTIFICATION]-(event)-[:NEXT*0..]-(evt)-[:LIKE_FROM|REPLY]-(user)
				RETURN labels(event), event.text, target.text, owner.name, user.name, event.timestamp as time
				ORDER BY time DESC'''%(vid)
		res = db.cypher.execute(cql)

		ret = []
		try:
			for r in res:
				ret.append({'event_type': r[0][0],
							'event_text': r[1],
							'target_text': r[2],
							'owner': r[3],
							'user': r[4],
							'time': r[5]})
		except:
			pass
		sf.write(json_encode({'ret':0, 'data':ret}))