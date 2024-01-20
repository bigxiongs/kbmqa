import json
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

DATA_PATH = 'test_subset.json'
