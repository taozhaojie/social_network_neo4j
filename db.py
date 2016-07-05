from py2neo import Graph, Path, authenticate
import settings

authenticate(settings.host, settings.username, settings.password)
graph = Graph(settings.host_link)
cypher = graph.cypher