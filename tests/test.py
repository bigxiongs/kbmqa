from datetime import date, datetime

import database.tuples as models

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

d = models.UserBase(username="user")
d = d._asdict()
print(d)
