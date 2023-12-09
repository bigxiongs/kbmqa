import unittest
from datetime import date, datetime

from ogm import *


class TestOGM(unittest.TestCase):
    rene = {
        "username": "rene",
        "password": "",
        "telephone": "",
        "email": "",
        "profile": "",
        "create_time": date(2000, 1, 1),
    }

    dialogue = {
        "creator": "rene",
        "did": "1",
        "title": "",
    }

    query = {
        "question": "",
        "answer": "",
        "create_time": datetime(2000, 1, 1, 0, 0, 0, 0),
    }

    def test_user(self):
        self.assertFalse(any(User.get(self.rene)))

        rene = User.create(self.rene)
        self.assertEqual(next(rene), self.rene)
        self.assertFalse(any(rene))

        rene = User.get(self.rene)
        self.assertEqual(next(rene), self.rene)
        self.assertFalse(any(rene))

        self.assertFalse(any(User.detach(self.rene)))
        self.assertFalse(any(User.get(self.rene)))

    def test_dialogue(self):
        self.assertFalse(any(User.get(self.rene)))

        rene = User.create(self.rene)
        self.assertEqual(next(rene), self.rene)
        self.assertFalse(any(rene))

        dialogue = Dialogue.create(self.dialogue)
        self.assertEqual(next(dialogue), self.dialogue)
        self.assertFalse(any(dialogue))

        dialogue = Dialogue.get(self.rene)
        self.assertEqual(next(dialogue), self.dialogue)
        self.assertFalse(any(dialogue))

        self.assertFalse(any(Dialogue.detach(self.dialogue)))
        self.assertFalse(any(Dialogue.get(self.rene)))

        self.assertFalse(any(User.detach(self.rene)))
        self.assertFalse(any(User.get(self.rene)))

    def test_query(self):
        self.assertFalse(any(User.get(self.rene)))
        User.create(self.rene)
        Dialogue.create(self.dialogue)

        temp = {**self.dialogue, **self.query}
        query = Query.create(temp)
        self.assertEqual(next(query), self.query)
        self.assertFalse(any(query))

        query = Query.get(self.dialogue)
        self.assertEqual(next(query), self.query)
        self.assertFalse(any(query))

        self.assertFalse(any(Query.detach(self.dialogue)))
        self.assertFalse(any(Query.get(self.dialogue)))

        self.assertFalse(any(Dialogue.detach(self.dialogue)))
        self.assertFalse(any(User.detach(self.rene)))


if __name__ == '__main__':
    unittest.main()
