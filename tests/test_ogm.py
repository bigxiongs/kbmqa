import unittest
from datetime import date, datetime

from ogm import *


class TestOGM(unittest.TestCase):
    user = {
        "type": "Node",
        "username": "user",
        "password": "",
        "telephone": "",
        "email": "",
        "profile": "",
        "create_time": date(2000, 1, 1),
    }

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
        self.assertFalse(any(User.get(self.user)))

        user = User.create(self.user)
        self.assertEqual(next(user)[0], self.user)
        self.assertFalse(any(user))

        user = User.get(self.user)
        self.assertEqual(next(user)[0], self.user)
        self.assertFalse(any(user))

        self.assertFalse(any(User.detach(self.user)))
        self.assertFalse(any(User.get(self.user)))

    def test_dialogue(self):
        self.assertFalse(any(User.get(self.user)))

        user = User.create(self.user)
        self.assertEqual(next(user)[0], self.user)
        self.assertFalse(any(user))

        dialogue = Dialogue.create(self.dialogue)
        self.assertEqual(next(dialogue)[0], self.dialogue)
        self.assertFalse(any(dialogue))

        dialogue = Dialogue.get(self.user)
        self.assertEqual(next(dialogue)[0], self.dialogue)
        self.assertFalse(any(dialogue))

        self.assertFalse(any(Dialogue.detach(self.dialogue)))
        self.assertFalse(any(Dialogue.get(self.user)))

        self.assertFalse(any(User.detach(self.user)))
        self.assertFalse(any(User.get(self.user)))

    def test_query(self):
        self.assertFalse(any(User.get(self.user)))
        User.create(self.user)
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
        self.assertFalse(any(User.detach(self.user)))


if __name__ == '__main__':
    unittest.main()
