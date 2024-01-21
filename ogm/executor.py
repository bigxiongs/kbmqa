import copy
from datetime import datetime

import ogm.tuples as models
from database.session import execute, Executor


class User:
    _get: Executor = execute("MATCH (u:User {username: $username}) RETURN u")
    """parameters: username"""

    _create: Executor = execute(
        "CREATE (u:User {username: $username, password: $password, telephone: $telephone, "
        "email: $email, profile: $profile, create_time: $create_time}) RETURN u")
    """parameters: username, password, telephone, email, profile, create_time"""

    _set_name: Executor = execute("MATCH (u:User {username: $username}) SET u.username = $new_name RETURN u")
    """parameters: username, new_name"""
    _set_password = execute("MATCH (u:User {username: $username}) SET u.password = $new_password RETURN u")
    """parameters: username, new_password"""

    _detach: Executor = execute("MATCH (u:User {username: $username}) DETACH DELETE u")
    """parameters: username"""

    _get_dialogues: Executor = execute("MATCH (:User {username: $username})-->(d:Dialogue) RETURN d")
    """parameters: username"""

    _get_graphs: Executor = execute("MATCH (:User {username: $username})-->(g:Graph) RETURN g")
    """parameters: username"""

    def __init__(self, user: models.UserBase | models.User | None):
        records = User._get(user._asdict()) if user is not None else []
        if isinstance(user, models.User) and len(records) == 0:
            records = User._create(user._asdict())
        self._instance = records
        self._dialogues = None
        self._graphs = None

    @property
    def _instance(self):
        return self._instance_real

    @_instance.setter
    def _instance(self, records):
        if len(records) == 0:
            self._instance_real = None
        elif len(records) == 1:
            self._instance_real = records[0]["u"]
        else:
            assert False

    def exists(self):
        return self._instance is not None

    @property
    def model(self) -> models.User | None:
        return None if self._instance is None else models.User(
            username=self.username,
            password=self.password,
            telephone=self.telephone,
            email=self.email,
            profile=self.profile,
            create_time=self.create_time,
        )

    @property
    def username(self):
        assert self._instance is not None
        return self._instance["username"]

    @username.setter
    def username(self, new_name: str):
        assert not User._get(models.UserBase(new_name)._asdict())
        records = User._set_name({"username": self.username, "new_name": new_name})
        self._instance = records

    @property
    def password(self):
        return self._instance["password"]

    @password.setter
    def password(self, new_password):
        records = User._set_password({"username": self.username, "new_password": new_password})
        self._instance = records

    @property
    def email(self):
        return self._instance["email"]

    @property
    def telephone(self):
        return self._instance["telephone"]

    @property
    def profile(self):
        return self._instance["profile"]

    @property
    def create_time(self):
        return self._instance["create_time"].to_native()

    @property
    def dialogues(self) -> list['Dialogue']:
        if self._dialogues is not None:
            return self._dialogues
        records = User._get_dialogues(models.UserBase(self.username)._asdict())
        dialogue_nodes = [r["d"] for r in records]
        dialogue_nodes = [models.Dialogue(d["creator"], d["did"], d["title"]) for d in dialogue_nodes]
        self._dialogues = [Dialogue(d) for d in dialogue_nodes]
        self._dialogues.sort(key=lambda d: d.did)
        return self.dialogues

    def open_dialogue(self, title: str):
        dialogue = models.Dialogue(self.username, len(self.dialogues), title)
        dialogue = Dialogue.open_dialogue(dialogue)
        self._dialogues.append(dialogue)

    def detach_dialogue(self, did: int):
        dialogues = [d for d in self.dialogues if d.did == did]
        assert len(dialogues) == 1
        dialogue = dialogues[0]
        dialogue.detach()
        self._dialogues = None

    def detach_dialogues(self):
        for d in self.dialogues:
            d.detach()
        self._dialogues = []

    @property
    def graphs(self) -> list['Graph']:
        if self._graphs is not None:
            return self._graphs
        records = User._get_graphs(models.UserBase(self.username)._asdict())
        graph_nodes = [r["g"] for r in records]
        graph_nodes = [models.Graph(g["creator"], g["gid"], g["title"], g["create_time"], g["edit_time"]) for g in
                       graph_nodes]
        self._graphs = [Graph(g) for g in graph_nodes]
        self._graphs.sort(key=lambda g: g.gid)
        return self.graphs

    def draw_graph(self, title: str, create_time: datetime, edit_time: datetime, gid=None):
        if gid is None:
            gid = len(self.graphs)
        graph = models.Graph(self.username, gid, title, create_time, edit_time)
        graph = Graph.draw_graph(graph)
        self._graphs.append(graph)

    def detach_graph(self, gid: int):
        graphs = [g for g in self.graphs if g.gid == gid]
        for graph in graphs:
            graph.detach()

    def detach_graphs(self):
        for graph in self.graphs:
            graph.detach()
        self._graphs = []

    def detach(self):
        assert self._instance is not None
        self.detach_dialogues()
        self.detach_graphs()
        User._detach(models.UserBase(self.username)._asdict())
        self._instance = None
        self._dialogues = None
        self._graphs = None

    def __eq__(self, __o):
        if __o is not User:
            return False
        return self.model == __o.model

    def __hash__(self):
        return hash(self.model)


class Dialogue:
    _create: Executor = execute(
        "MATCH (u:User {username: $creator}) "
        "CREATE (u)-[:OPEN]->(d:Dialogue {creator: $creator, did: $did, title: $title}) return d")
    """parameters: creator, did, title"""

    _get_history: Executor = execute(
        "MATCH (d:Dialogue {creator: $creator, did: $did})-->(q:Query) return q")
    """parameters: creator, did"""

    _set_title = execute("MATCH (d:Dialogue {creator: $creator, did: $did}) SET d.title = $title RETURN d")

    _create_query = execute(
        "MATCH (d:Dialogue {creator: $creator, did: $did}) "
        "CREATE (d)-[:CONTAIN]->(q:Query {question: $question, answer: $answer, create_time: $create_time})")

    _detach_queries: Executor = execute("MATCH (d:Dialogue {creator: $creator, did: $did})-->(q:Query) DETACH DELETE q")
    _detach: Executor = execute("MATCH (d:Dialogue {creator: $creator, did: $did}) DETACH DELETE d")

    def __init__(self, dialogue: models.Dialogue):
        self._instance = None
        self._history = None
        if dialogue is not None:
            self._creator = dialogue.creator
            self._did = dialogue.did
            self._title = dialogue.title

    @property
    def model(self) -> models.Dialogue:
        return models.Dialogue(self.creator, self.did, self.title)

    @property
    def creator(self):
        return self._creator

    @property
    def did(self):
        return self._did

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        Dialogue._set_title(models.Dialogue(self.creator, self.did, new_title)._asdict())
        self._title = new_title

    @property
    def history(self) -> list['Query']:
        if self._history is not None:
            return self._history
        records = Dialogue._get_history(models.DialogueBase(self.creator, self.did)._asdict())
        queries = [r["q"] for r in records]
        queries = [models.Query(q["question"], q["answer"], q["create_time"]) for q in queries]
        self._history = [Query(q) for q in queries]
        self._history.sort(key=lambda h: h.create_time)
        return self.history

    def detach(self):
        Dialogue._detach_queries(models.DialogueBase(self.creator, self.did)._asdict())
        Dialogue._detach(models.DialogueBase(self.creator, self.did)._asdict())

    @staticmethod
    def open_dialogue(dialogue: models.Dialogue) -> 'Dialogue':
        records = Dialogue._create(dialogue._asdict())
        dialogue = records[0]["d"]
        return Dialogue(models.Dialogue(dialogue["creator"], dialogue["did"], dialogue["title"]))

    def continue_dialogue(self, question: str, answer: str):
        query = models.Query(question, answer, datetime.now())
        Dialogue._create_query(self.model._asdict() | query._asdict())
        self._history = None
        return self.history[-1]

    def __eq__(self, __o):
        if __o is not Dialogue:
            return False
        return self.model == __o.model

    def __hash__(self):
        return hash(self.model)


class Query:
    _create: Executor = execute(
        "MATCH (d:Dialogue {did: $did, creator: $creator}) "
        "CREATE (d)-[:CONTAIN]->(q:Query {question: $question, answer: $answer, create_time: $create_time})"
        "RETURN q")
    """parameters: did, creator, question, answer, create_time"""

    _get: Executor = execute("MATCH (d:Dialogue {did: $did})-->(q:Query) RETURN q")
    """parameters: did"""

    _detach: Executor = execute("MATCH (:Dialogue {did: $did})-->(q:Query) DETACH DELETE q")
    """parameters: did"""

    def __init__(self, query: models.Query | None):
        self._instance = None
        if query is not None:
            self.question = query.question
            self.answer = query.answer
            self.create_time = query.create_time

    @property
    def model(self) -> models.Query:
        return models.Query(self.question, self.answer, self.create_time)

    def __eq__(self, __o):
        if __o is not Query:
            return False
        return self.model == __o.model

    def __hash__(self):
        return hash(self.model)


class Graph:
    _create: Executor = execute(
        "MATCH (u:User {username: $creator}) CREATE (u)-[:CREATE]->(g:Graph {gid: $gid, title: $title, "
        "creator: $creator, create_time: $create_time, edit_time: $edit_time}) return g")
    """parameters: creator, gid, title, create_time, edit_time"""

    _create_knowledge_node_stmt = "MATCH (g:Graph {creator: $creator, gid: $gid}) CREATE (g)-[:CONTAIN]->(k:? {?})"
    _create_knowledge_relationship_stmt = ("MATCH (g:Graph {creator: $creator, gid: $gid})-->(k1 {kid: $start_node}) "
                                           "MATCH (g)-->(k2 {kid: $end_node}) CREATE (k1)-[:??]->(k2)")

    _set_edit_time = execute("MATCH (g:Graph {creator: $creator, gid: $gid}) SET g.edit_time = $edit_time RETURN g")

    _detach_knowledge = execute("MATCH (g:Graph {creator: $creator, gid: $gid})-[:CONTAIN]->(k) DETACH DELETE k")
    _detach = execute("MATCH (g:Graph {creator: $creator, gid: $gid}) DETACH DELETE g")

    _get_knowledge_node = execute("MATCH (g:Graph {creator: $creator, gid: $gid})-->(k) return k")
    _get_knowledge_node_by_name_stmt = "MATCH (g:Graph {creator: $creator, gid: $gid})-->(k? {name: $name}) return k"
    _get_knowledge_relationship = execute(
        "MATCH (g:Graph {creator: $creator, gid: $gid})-->(k1)-[r]->(k2) return k1, k2, r")

    def __init__(self, graph: models.Graph):
        self._instance = None
        self._knowledge_nodes = None
        self._knowledge_relationships = None
        if graph is not None:
            self.creator = graph.creator
            self.gid = graph.gid
            self.title = graph.title
            self.create_time = graph.create_time
            self._edit_time = graph.edit_time

    @property
    def model(self):
        return models.Graph(self.creator, self.gid, self.title, self.create_time, self.edit_time)

    @property
    def model_base(self):
        return models.GraphBase(self.creator, self.gid)


    @property
    def edit_time(self):
        return self._edit_time


    @edit_time.setter
    def edit_time(self, t: datetime):
        records = Graph._set_edit_time(self.model_base._asdict() | {"edit_time": t})
        self._edit_time = t

    @property
    def knowledge(self):
        return self.knowledge_nodes + self.knowledge_relationships

    @property
    def knowledge_nodes(self) -> list[models.KNode]:
        if self._knowledge_nodes is not None:
            return self._knowledge_nodes
        records = Graph._get_knowledge_node(models.GraphBase(self.creator, self.gid)._asdict())
        k_nodes = [r["k"] for r in records]
        k_nodes = [models.KNode(node.labels, node.items()) for node in k_nodes]
        self._knowledge_nodes = k_nodes
        self._knowledge_nodes.sort(key=lambda n: n.kid)
        return self.knowledge_nodes

    def find_node(self, labels: list[str], name: str) -> models.KNode:
        stmt = Graph._get_knowledge_node_by_name_stmt
        stmt = stmt.replace("?", ":" + ":".join(labels) if labels else "")
        records = execute(stmt)(models.GraphBase(self.creator, self.gid)._asdict() | {"name": name})
        k_node = [r["k"] for r in records][0]
        return models.KNode(list(k_node.labels), dict(k_node.items()))

    @property
    def knowledge_relationships(self) -> list[models.KRelationship]:
        if self._knowledge_relationships is not None:
            return self._knowledge_relationships
        records = Graph._get_knowledge_relationship(models.GraphBase(self.creator, self.gid)._asdict())
        k_rels = [r["r"] for r in records]
        k_rels = [models.KRelationship(rel.type, dict(rel.items()), rel.start_node["kid"], rel.end_node["kid"]) for rel
                  in k_rels]
        self._knowledge_relationships = k_rels
        return self.knowledge_relationships

    def draw_node(self, node: models.KNode):
        node = copy.deepcopy(node)
        node.properties["kid"] = len(self.knowledge_nodes)
        stmt = self._create_knowledge_node_stmt
        stmt = stmt.replace("?", ":".join(node.labels), 1)
        stmt = stmt.replace("?", ", ".join(f"{k}: ${k}" for k in node.properties))
        execute(stmt)(self.model_base._asdict() | node.properties)
        self._edit_time = datetime.now()
        self._knowledge_nodes.append(node)

    def draw_relationship(self, relationship: models.KRelationship):
        relationship = copy.deepcopy(relationship)
        rel = {"start_node": relationship.start_node, "end_node": relationship.end_node}
        stmt = self._create_knowledge_relationship_stmt
        stmt = stmt.replace("?", relationship.type, 1)
        if relationship.properties:
            stmt = stmt.replace("?", " {?}", 1)
            stmt = stmt.replace("?", ", ".join(f"{k}: ${k}" for k in relationship.properties))
        else:
            stmt = stmt.replace("?", "")
        execute(stmt)(self.model_base._asdict() | relationship.properties | rel)
        self._edit_time = datetime.now()
        _ = self.knowledge_relationships

    def detach(self):
        Graph._detach_knowledge(models.GraphBase(self.creator, self.gid)._asdict())
        Graph._detach(models.GraphBase(self.creator, self.gid)._asdict())

    @staticmethod
    def draw_graph(graph: models.Graph) -> 'Graph':
        records = Graph._create(graph._asdict())
        graph = records[0]["g"]
        return Graph(
            models.Graph(graph["creator"], graph["gid"], graph["title"], graph["create_time"], graph["edit_time"]))
