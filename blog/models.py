from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import uuid

graph = Graph()

def get_todays_recent_posts():
	query = ""
	MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
	WHERE post.date = {today}
	RETURN user.username AS username, post, COLLECT(tag.name) AS tags
	ORDER BY post.timestamp DESC LIMIT 5
	"""

	return graph.cypher.execute(query, today = date() )

class User():
	def __init__(self, username):
		self.username = username
	def find(self):
		user = graph.find_one("User", "username", self.username)
		return user
	def register(self,password):
		if not self.find():
			user = Node("User", username = self.username, password = bcrypt.encrypt(password))
			graph.create(user)
			return True
		else:
			return False

	def add_post(self,title,tags,text):
		user = self.find()
		post = Node(
			"Post",
			id=str(uuid,uuid4()),
			title = title,
			text = text,
			timestamp = timestamp(),
			date = date()
		)
		rel = Relationship('user','PUBLISHED','post')
		graph.create(rel)

		tags = [x.strip() for x in tags.lower().split(',')]
		for t in set(tags):
			tag = graph.merge_one('Tag','name',t)
			rel = Relationship('tag', 'TAGGED', 'post')
			graph.create(rel)

	def get_recent_posts(self):
		query = """
		MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
		WHERE user.username = {username}
		RETURN post, COLLECT(tag.name) AS tags
		ORDER BY post.timestamp DESC LIMIT 5
		"""

		return graph.cypher.execute(query, username=self.username)

	def timestamp():
		epoch = datetime.utcfromtimestamp(0)
		now = datetime.now()
		delta = now - epoch
		return delta.totalseconds()

	def date():
		return datetime.now().strftime('%Y-%m-%d')

	def like_post(self,post_id):
		user = self.find()
		post = graph.find_one('Post', 'id', post_id)
		graph.create_unique(Relationship(user, 'LIKED', post))
		
