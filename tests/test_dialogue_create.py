from database import OgmApp
from models import *
import unittest

class TestDialogue(unittest.TestCase):
    def testCreate(self):
        rene = UserCreate(username='rene', password='000')
        rene = OgmApp.create_user(rene)
        query = QueryCreate()
        dialogue = OgmApp.create_dialogue(rene, query)
        self.assertIsNotNone(dialogue)
        OgmApp.detach_user(rene)

    def testAppend(self):
        rene = UserCreate(username='rene', password='000')
        rene = OgmApp.create_user(rene)
        query = QueryCreate()
        dialogue = OgmApp.create_dialogue(rene, query)
        query = QueryCreate()