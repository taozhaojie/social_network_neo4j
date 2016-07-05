import db
import uuid
import function
from tornado import gen

class Moment(object):
	def __init__(self,vid,action):
		self.vid = vid
		self.action = action

	@classmethod
	def list(self,sf):
		sf.write('123')

	@classmethod
	@gen.coroutine
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
		res = yield db.cypher.execute(cql)
		print '#', res

