import unittest
from datetime import date, datetime

from ogm import *
import database.tuples as models


class TestOGM(unittest.TestCase):
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
        "title": "",
    }

    query = {
        "type": "Node",
        "question": "",
        "answer": "",
        "create_time": datetime(2000, 1, 1, 0, 0, 0, 0),
    }

    def test_user(self):
        user = User(self.user_get)
        self.assertIsNone(user.info)

        user = User(self.user_create)
        self.assertEqual(user.info, self.user_create)

        user = User(self.user_get)
        self.assertEqual(user.info, self.user_create)

        user = user.detach()
        self.assertIsNone(user.info)

    def test_dialogue(self):
        self.assertFalse(any(User._get(self.user_create)))

        user = User._create(self.user_create)
        self.assertEqual(next(user)[0], self.user_create)
        self.assertFalse(any(user))

        dialogue = Dialogue.create(self.dialogue)
        self.assertEqual(next(dialogue)[0], self.dialogue)
        self.assertFalse(any(dialogue))

        dialogue = Dialogue.get(self.user_create)
        self.assertEqual(next(dialogue)[0], self.dialogue)
        self.assertFalse(any(dialogue))

        self.assertFalse(any(Dialogue.detach(self.dialogue)))
        self.assertFalse(any(Dialogue.get(self.user_create)))

        self.assertFalse(any(User._detach(self.user_create)))
        self.assertFalse(any(User._get(self.user_create)))

    def test_query(self):
        self.assertFalse(any(User._get(self.user_create)))
        User._create(self.user_create)
        Dialogue.create(self.dialogue)

        temp = {**self.dialogue, **self.query}
        query = Query.create(temp)
        self.assertEqual(next(query)[0], self.query)
        self.assertFalse(any(query))

        query = Query.get(self.dialogue)
        self.assertEqual(next(query)[0], self.query)
        self.assertFalse(any(query))

        self.assertFalse(any(Query.detach(self.dialogue)))
        self.assertFalse(any(Query.get(self.dialogue)))

        self.assertFalse(any(Dialogue.detach(self.dialogue)))
        self.assertFalse(any(User._detach(self.user_create)))


if __name__ == '__main__':
    unittest.main()
