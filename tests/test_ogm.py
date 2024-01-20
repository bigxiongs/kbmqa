import unittest
from datetime import date

from ogm import *


class TestOGM(unittest.TestCase):
    datetime = datetime(2000, 1, 1, 0, 0, 0, 0)
    date = date(2000, 1, 1)

    user_create = models.User("user", "", "", "", "", date)
    user_base = models.UserBase("user")
    user_new_name = models.UserBase("new_user")
    user_new_name_create = models.User("new_user", "", "", "", "", date)

    test_dialogue = models.Dialogue("user", 0, "test dialogue")

    query_create = models.Query("q", "a", datetime)

    graph_create = models.Graph("user", 0, "test graph", datetime, datetime)
    knowledge_create = models.KNode(["equipment"], {"country": "China"})
    knowledge_1 = models.KNode(["equipment"], {"kid": 0, "country": "China", "name": "one"})
    knowledge_2 = models.KNode(["equipment"], {"kid": 1, "country": "China", "name": "two"})
    knowledge_3 = models.KNode(["equipment"], {"kid": 2, "country": "China", "name": "three"})
    knowledge_rel_1 = models.KRelationship("RELATE", {}, 0, 1)

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
        self.assertTrue(all(a == b for a, b in zip([d.model for d in user.dialogues], [self.test_dialogue])))

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
        self.assertTrue(all(a == b for a, b in zip([q.model for q in dialogue.history], [self.query_create])))

        user.detach_dialogues()
        self.assertEqual(len(user.dialogues), 0)

        user = user.detach()
        self.assertIsNone(user.model)

    def test_graph_create(self):
        user = User(self.user_create)
        self.assertEqual(user.model, self.user_create)

        user.draw_graph("test graph", self.datetime, self.datetime)
        for a, b in zip([g.model for g in user.graphs], [self.graph_create]):
            self.assertEqual(a, b)

        user.detach_graphs()
        self.assertEqual(len(user.dialogues), 0)

        user = user.detach()
        self.assertIsNone(user.model)

    def test_graph_create_with_knowledge(self):
        user = User(self.user_create)
        self.assertEqual(user.model, self.user_create)
        user.draw_graph("test graph", self.datetime, self.datetime)

        graph = user.graphs[0]
        graph.draw_node(self.knowledge_create)
        graph.draw_node(self.knowledge_create)
        graph.draw_node(self.knowledge_create)
        self.assertEqual(graph.knowledge_nodes[0], self.knowledge_1)
        self.assertEqual(graph.knowledge_nodes[1], self.knowledge_2)
        self.assertEqual(graph.knowledge_nodes[2], self.knowledge_3)

        graph.draw_relationship(self.knowledge_rel_1)
        self.assertEqual(graph.knowledge_relationships[0], self.knowledge_rel_1)

        user = user.detach()
        self.assertIsNone(user.model)

    def test_find_node_in_graph(self):
        user = User(self.user_create)
        self.assertEqual(user.model, self.user_create)
        user.draw_graph("test graph", self.datetime, self.datetime)

        graph = user.graphs[0]
        graph.draw_node(self.knowledge_1)
        graph.draw_node(self.knowledge_2)
        graph.draw_node(self.knowledge_3)
        self.assertEqual(graph.find_node(["equipment"], "one"), self.knowledge_1)
        self.assertEqual(graph.find_node(["equipment"], "two"), self.knowledge_2)
        self.assertEqual(graph.find_node(["equipment"], "three"), self.knowledge_3)

        user = user.detach()
        self.assertIsNone(user.model)


if __name__ == '__main__':
    unittest.main()
