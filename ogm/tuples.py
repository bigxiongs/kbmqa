from collections import namedtuple

UserBase = namedtuple("UserBase", ["username"])
"""Base Model of User. Username is the unique identifier of a user."""
User = namedtuple("User", ["username", "password", "telephone", "email", "profile", "create_time"])
"""User Model"""

Query = namedtuple("Query", ["question", "answer", "create_time"])
"""Base model of Query. Queries are detached with a dialogue through [:CONTAIN]."""
Dialogue = namedtuple("Dialogue", ["creator", "did", "title"])
"""Dialogue Model"""
DialogueBase = namedtuple("DialogueBase", ["creator", "did"])
"""A Dialogue represent a sequence of queries as well as other properties, who are then [:OPEN] to a user."""

Graph = namedtuple("Graph", ["creator", "gid", "title", "create_time", "edit_time"])
"""Graph Model"""
GraphBase = namedtuple("GraphBase", ["creator", "gid"])
"""A Graph is [:DRAW] by a user, and contains list of knowledge nodes and relationships which form a knowledge graph."""

KNode = namedtuple("KnowledgeNode", ["labels", "properties"])
"""When create a knowledge node, the properties should not contain GraphBase/kid."""
KRelationship = namedtuple("KnowledgeRelationship", ["type", "properties", "start_node", "end_node"])
"""When create a knowledge relationship, the properties should not contain GraphBase."""
