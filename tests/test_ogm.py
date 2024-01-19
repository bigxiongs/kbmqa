import unittest
from datetime import date, datetime

from ogm import *
import database.tuples as models


class TestOGM(unittest.TestCase):
    user_create = models.User("user", "", "", "", "", date(2000, 1, 1))
    user_base = models.UserBase("user")
    user_new_name = models.UserBase("new_user")
    user_new_name_create = models.User("new_user", "", "", "", "", date(2000, 1, 1))

    test_dialogue = models.Dialogue("user", 0, "test dialogue")

    query_create = models.Query("q", "a", datetime(2000, 1, 1, 0, 0, 0, 0))

    def test_user_create(self):
        user = User(self.user_base)
        self.assertIsNone(user.model)

        user = User(self.user_create)
        self.assertEqual(user.model, self.user_create)

        user = User(self.user_base)
        self.assertEqual(user.model, self.user_create)

        user = user.detach()
        self.assertIsNone(user.model)

    def test_user_set_username(self):
        user = User(self.user_create)
        self.assertEqual(user.model, self.user_create)

        user.username = self.user_new_name.username
        self.assertEqual(user.model, self.user_new_name_create)

        user.username = self.user_base.username

        user = user.detach()
        self.assertIsNone(user.model)

    def test_dialogue_create(self):
        user = User(self.user_create)
        self.assertEqual(user.model, self.user_create)

        user.open_dialogue("test dialogue")
        for a, b in zip([d.model for d in user.dialogues], [self.test_dialogue]):
            self.assertEqual(a, b)

        user.detach_dialogues()
        self.assertEqual(len(user.dialogues), 0)

        user = user.detach()
        self.assertIsNone(user.model)

    def test_query_create(self):
        user = User(self.user_create)
        self.assertEqual(user.model, self.user_create)

        user.open_dialogue("test dialogue")
        dialogue = user.dialogues[0]
        dialogue.continue_dialogue(self.query_create)
        for a, b in zip([q.model for q in dialogue.history], [self.query_create]):
            self.assertEqual(a, b)

        user.detach_dialogues()
        self.assertEqual(len(user.dialogues), 0)

        user = user.detach()
        self.assertIsNone(user.model)


if __name__ == '__main__':
    unittest.main()
