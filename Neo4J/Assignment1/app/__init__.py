from .views import app
from .models import graph

graph.schema.create_uniqueness_constraint("Author", "author_id")
graph.schema.create_uniqueness_constraint("Tweet", "tid")
