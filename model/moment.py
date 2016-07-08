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
				WITH latest_update, collect(secondlatestupdate) AS seconds, me
				FOREACH (x IN seconds | CREATE (latest_update)-[:NEXT]->(x))
				WITH latest_update, me
				OPTIONAL MATCH (me)-[r:SUBS_FROM]-(secondsubs)
				DELETE r
				CREATE (me)-[:SUBS_FROM]->(latest_subs:SUBSCRIBLE {timestamp:%i})
				WITH latest_subs, latest_update, collect(secondsubs) as secs
				CREATE (latest_subs)-[:SUBS_TO]->(latest_update)
				WITH secs, latest_subs
				FOREACH (x IN secs | CREATE (latest_subs)-[:NEXT]->(x))
				'''%(uid, uuid.uuid4(), text, function.timestamp(), function.timestamp())
		print cql
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
				WITH collect(friends)+collect(distinct(me)) as user
				UNWIND user as users
				MATCH (users)-[:POST]-(latestpost)-[:NEXT*%i..%i]-(posts)
				RETURN users.uid, users.name, posts.text, posts.id, posts.timestamp as timestamp
				ORDER BY timestamp DESC'''%(uid,page_start,page_end)
		res = db.cypher.execute(cql)

		ret = []
		try:
			for r in res:
				ret.append({'uid': r[0], 'name': r[1], 'text': r[2], 'id': r[3], 'time': r[4]})
		except:
			pass

		sf.write(json_encode({'ret':0, 'data':ret}))

	@classmethod
	def like(self,vid,uid,sf):
		vid = str(vid)
		uid = str(uid)
		cql = '''
				MATCH (me)
				WHERE me.uid=%s
				OPTIONAL MATCH (me)-[r:LIKE_FROM]-(secondlatestupdate)
				DELETE r
				CREATE (me)-[:LIKE_FROM]->(latest_update:LIKE {timestamp:%i})
				WITH latest_update, collect(secondlatestupdate) AS seconds
				FOREACH (x IN seconds | CREATE (latest_update)-[:NEXT]->(x))
				WITH latest_update
				MATCH (evt:Event {id: '%s'})
				CREATE (latest_update)-[:LIKE_TO]->(evt)
				RETURN evt.id AS uuid'''%(uid, function.timestamp(), vid)
		res = db.cypher.execute(cql)

		temp_id = res[0][0]

		cql = '''
				MATCH(me)
				WHERE me.uid=%s
				MATCH (me)-[r:SUBS_FROM]-(subs)-[:SUBS_TO]-(evt:Event {id:'%s'})
				RETURN COUNT(r)
				'''%(uid, temp_id)
		res = db.cypher.execute(cql)

		if res[0][0] == 0:
			cql = '''
					MATCH(me)
					WHERE me.uid=%s
					OPTIONAL MATCH (me)-[r:SUBS_FROM]-(secondlatestupdate)
					DELETE r
					CREATE (me)-[:SUBS_FROM]->(latest_update:SUBSCRIBLE {timestamp:%i})
					WITH latest_update, collect(secondlatestupdate) AS seconds
					MATCH (evt)
					WHERE evt.id='%s'
					WITH latest_update, seconds, evt
					CREATE (latest_update)-[:SUBS_TO]->(evt)
					WITH latest_update, seconds
					FOREACH (x IN seconds | CREATE (latest_update)-[:NEXT]->(x))'''%(uid, function.timestamp(), temp_id)
			print cql
			res = db.cypher.execute(cql)

	@classmethod
	def liked(self,vid,sf):
		vid = str(vid)
		cql = '''
				MATCH (evt:Event {id:'%s'})-[r:LIKE_TO]-(likes)-[:LIKE_FROM]-(users)
				RETURN users'''%(vid)
		res = db.cypher.execute(cql)

		ret = []
		try:
			for r in res:
				ret.append(r[0].properties)
		except:
			pass
		sf.write(json_encode({'ret':0, 'data':ret}))

	@classmethod
	def reply(self,vid,text,uid,sf):
		uid = str(uid)
		cql = '''
				MATCH (me)
				WHERE me.uid=%s
				OPTIONAL MATCH (me)-[r:REPLY]-(secondlatestupdate)
				DELETE r
				CREATE (me)-[:REPLY]->(latest_update:Event {id:'%s', text:'%s', timestamp:%i})
				WITH latest_update, collect(secondlatestupdate) AS seconds
				FOREACH (x IN seconds | CREATE (latest_update)-[:NEXT]->(x))
				WITH latest_update
				MATCH (evt:Event {id: '%s'})
				CREATE (latest_update)-[:REPLY_TO]->(evt)
				RETURN latest_update.id as uuid'''%(uid, uuid.uuid4(), text, function.timestamp(), vid)
		res = db.cypher.execute(cql)

		temp_id = res[0][0]

		cql = '''
				MATCH(me)
				WHERE me.uid=%s
				MATCH (evt:Event {id:'%s'})-[:REPLY_TO*]->(root_evt)
				WITH root_evt, me
				MATCH (me)-[r:SUBS_FROM]-(subs)-[:SUBS_TO]-(root_evt)
				RETURN COUNT(r)
				'''%(uid, temp_id)
		res = db.cypher.execute(cql)

		if res[0][0] == 0:
			cql = '''
					MATCH(me)
					WHERE me.uid=%s
					MATCH (evt:Event {id:'%s'})-[:REPLY_TO*]-(evts)-[:REPLY_TO]->(root_evt)
					WITH root_evt, me
					ORDER BY root_evt.timestamp
					LIMIT 1
					OPTIONAL MATCH (me)-[r:SUBS_FROM]-(secondlatestupdate)
					DELETE r
					CREATE (me)-[:SUBS_FROM]->(latest_update:SUBSCRIBLE {timestamp:%i})
					WITH latest_update, root_evt, collect(secondlatestupdate) AS seconds
					CREATE (latest_update)-[:SUBS_TO]->(root_evt)
					WITH latest_update, seconds
					FOREACH (x IN seconds | CREATE (latest_update)-[:NEXT]->(x))'''%(uid, temp_id, function.timestamp())
			res = db.cypher.execute(cql)

	@classmethod
	def reply_get(self,vid,sf):
		vid = str(vid)
		cql = '''
				MATCH (evt:Event {id:'%s'})-[r:REPLY_TO*0..]-(related_events)-[:NEXT*0..]-(other_replies)-[:REPLY|POST]-(replied_from)
				WITH related_events, replied_from
				MATCH (related_events)-[:REPLY_TO]->(replied_events)-[:NEXT*0..]-(other_replies)-[:REPLY|POST]-(replied_to)
				RETURN  related_events.id, replied_events.id, related_events.text, replied_from.uid, replied_to.uid, replied_from.name, replied_to.name, related_events.timestamp as time
				ORDER BY time'''%(vid)
		res = db.cypher.execute(cql)

		ret = []
		try:
			for r in res:
				ret.append({'reply_from': r[0],
							'reply_to': r[1],
							'text': r[2],
							'user_from': r[3],
							'user_to': r[4],
							'user_from_name': r[5],
							'user_to_name': r[6],
							'time': r[7]})
		except:
			pass
		sf.write(json_encode({'ret':0, 'data':ret}))