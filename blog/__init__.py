from .views import app
from .models import graph

def create_uniqeness_constraint(label,property):
	query = "CREATE CONSTRAINT ON (n:{label}) ASSERT n.{property} IS UNIQUE"
	query = query.format(label=label,property=property)
	graph.cypher.execute(query)

create_uniqeness_constraint("User","username")
create_uniqeness_constraint("Post","id")
create_uniqeness_constraint("Tag","name")
