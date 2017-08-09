from py2neo import Graph, Node, Relationship, authenticate
from passlib.hash import bcrypt
from datetime import datetime
import uuid

authenticate("localhost:7474", "neo4j", "abc123XYZ!")
graph_db = Graph("http://localhost:7474/db/data/")
graph = Graph()

def get_todays_recent_posts():
	query = '''
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE post.date = {today}
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
	'''

	return graph.cypher.execute(query, today = date())

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

	def get_similar_users(self):
		# find 3 users similar to me based on similar tags
		query = """
		MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
		(they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
		WHERE you.username = {username} AND you <> they
		WITH they, COLLECT(DISTINCT tag.name) AS tags
		ORDER BY SIZE (tags), DESC LIMIT 3
		RETURN they.username AS similar_user, tags
		"""

		return graph.cypher.execute(query, username = self.username)

	def get_commonality_of_users(self, other):
		# find out how many of the logged in users posts the other user has liked
		# and which tags they both write about
		query = """
		MATCH (they:User {username: {they} })
		MATCH (you:User {username: {you} })
		OPTIONAL MATCH (they)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
		(you)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
		RETURN SIZE ((they)-[:LIKED]->(:Post)<-[:PUBLISHED]-(you)) AS likes,
		COLLECT (DISTINCT tag.name) AS tags
		"""

		return graph.cypher.query(query,they=other.username,you=self.username)[0]
