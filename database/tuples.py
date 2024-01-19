from collections import namedtuple

UserBase = namedtuple("UserBase", ["username"])
User = namedtuple("User", ["username", "password", "telephone", "email", "profile", "create_time"])

Query = namedtuple("Query", ["question", "answer", "create_time"])
Dialogue = namedtuple("Dialogue", ["creator", "did", "title"])
DialogueBase = namedtuple("DialogueBase", ["creator", "did"])

Graph = namedtuple("Graph", ["creator", "gid", "title", "create_time", "edit_time"])
GraphBase = namedtuple("GraphBase", ["creator", "gid"])

KNode = namedtuple("KnowledgeNode", ["labels", "properties"])
KRelationship = namedtuple("KnowledgeRelationship", ["type", "properties", "start_node", "end_node"])
