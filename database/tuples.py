from collections import namedtuple

UserBase = namedtuple("UserBase", ["username"])
User = namedtuple("User", ["username", "password", "telephone", "email", "profile", "create_time"])

Query = namedtuple("Query", ["question", "answer", "create_time"])
Dialogue = namedtuple("Dialogue", ["did", "title", "history"])
