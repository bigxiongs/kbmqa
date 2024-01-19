from datetime import date, datetime

from ogm import *

user_create = models.User(**{
        "username": "user",
        "password": "",
        "telephone": "",
        "email": "",
        "profile": "",
        "create_time": date(2000, 1, 1),
})

user_get = models.UserBase(username="user")

dialogue = {
    "type": "Node",
    "creator": "user",
    "did": "1",
    "title": "", }

query = {
    "type": "Node",
    "question": "",
    "answer": "",
    "create_time": datetime(2000, 1, 1, 0, 0, 0, 0), }

records = Graph._get_knowledge_node(models.GraphBase("rene", 1)._asdict())
knowledge_nodes = [r["k"] for r in records]
knowledge_nodes = [models.KNode(**k) for k in knowledge_nodes]
