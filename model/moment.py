import db
import function
from tornado import gen
import uuid
from tornado.escape import json_encode

class Moment(object):
	def __init__(self,vid,action):
		self.vid = vid
		self.action = action

	@classmethod
	def list(self,sf):
		sf.write('123')

	@classmethod
	def create(self,text,uid,sf):
		uid = str(uid)
		cql = '''
				MATCH (me)
				WHERE me.uid=%s
				OPTIONAL MATCH (me)-[r:POST]-(secondlatestupdate)
				DELETE r
				CREATE (me)-[:POST]->(latest_update:Event {id:'%s', text:'%s', timestamp:%i})
				WITH latest_update, collect(secondlatestupdate) AS seconds
				FOREACH (x IN seconds | CREATE (latest_update)-[:NEXT]->(x))
				RETURN latest_update.text AS new_status'''%(uid, uuid.uuid4(), text, function.timestamp())
		res = db.cypher.execute(cql)
		print '#', res

	@classmethod
	def list(self,uid,page,sf):
		uid = str(uid)
		page = int(page)
		page_start = page * 20
		page_end = page * 20 + 19
		cql = '''
				MATCH (me)
				WHERE me.uid=%s
				OPTIONAL MATCH (me)-[r:FRIEND]-(friends)
				WITH friends
				MATCH (friends)-[:POST]-(latestpost)-[:NEXT*%i..%i]-(posts)
				RETURN friends.uid, friends.name, posts.text, posts.id, posts.timestamp as timestamp
				ORDER BY timestamp DESC'''%(uid,page_start,page_end)
		res = db.cypher.execute(cql)

		ret = []
		try:
			for r in res:
				ret.append({'uid': r[0], 'name': r[1], 'text': r[2], 'id': r[3], 'time': r[4]})
		except:
			pass

		sf.write(json_encode({'ret':0, 'data':ret}))
