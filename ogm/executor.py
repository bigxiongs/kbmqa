import database.tuples as models
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

    _detach: Executor = execute("MATCH (u:User {username: $username}) DETACH DELETE u")
    """parameters: username"""

    _get_dialogues: Executor = execute("MATCH (:User {username: $username})-->(d:Dialogue) RETURN d")
    """parameters: username"""

    _get_graphs: Executor = execute("MATCH (:User {username: $username})-->(g:Graph) RETURN g")
    """parameters: username"""

    def __init__(self, user: models.UserBase | models.User | None):
        records = User._get(user._asdict()) if user is not None else []
        if isinstance(user, models.User):
            assert len(records) == 0, "user already exists"
            records = User._create(user._asdict())
        self._info = records
        self._dialogues = None
        self._graphs = None

    @property
    def _info(self):
        return self._instance

    @_info.setter
    def _info(self, records):
        if len(records) == 0:
            self._instance = None
        elif len(records) == 1:
            self._instance = records[0]["u"]
        else:
            assert False

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
        return self._info["username"]

    @username.setter
    def username(self, new_name: str):
        assert not User._get(models.UserBase(new_name)._asdict())
        records = User._set_name({"username": self.username, "new_name": new_name})
        self._info = records

    @property
    def password(self):
        return self._info["password"]

    @property
    def email(self):
        return self._info["email"]

    @property
    def telephone(self):
        return self._info["telephone"]

    @property
    def profile(self):
        return self._info["profile"]

    @property
    def create_time(self):
        return self._info["create_time"].to_native()

    @property
    def dialogues(self) -> list['Dialogue']:
        if self._dialogues is not None:
            return self._dialogues
        records = User._get_dialogues(models.UserBase(self.username)._asdict())
        dialogue_nodes = [r["d"] for r in records]
        dialogue_nodes = [models.Dialogue(d["creator"], d["did"], d["title"]) for d in dialogue_nodes]
        self._dialogues = [Dialogue(d) for d in dialogue_nodes]
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
    def graphs(self):
        if self._graphs is not None:
            return self._graphs
        records = User._get_graphs(models.UserBase(self.username)._asdict())
        graph_nodes = [r["g"] for r in records]
        graph_nodes = [models.Graph(g["creator"], g["gid"], g["title"], g["create_time"], g["edit_time"]) for g in
                       graph_nodes]
        self._graphs = [Graph(g) for g in graph_nodes]

    def detach_graph(self, gid: int):
        graphs = [g for g in self.graphs if g.gid == gid]
        assert len(graphs) == 1
        graph = graphs[0]
        graph.detach()

    def detach_graphs(self):
        for graph in self.graphs:
            graph.detach()

    def detach(self):
        if self._info is not None:
            User._detach(models.UserBase(self.username)._asdict())
            return User(models.UserBase(self.username))
        assert False

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
    def model(self):
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
        return self.history

    def detach(self):
        Dialogue._detach_queries(models.DialogueBase(self.creator, self.did)._asdict())
        Dialogue._detach(models.DialogueBase(self.creator, self.did)._asdict())

    @staticmethod
    def open_dialogue(dialogue: models.Dialogue) -> 'Dialogue':
        records = Dialogue._create(dialogue._asdict())
        dialogue = records[0]["d"]
        return Dialogue(models.Dialogue(dialogue["creator"], dialogue["did"], dialogue["title"]))

    def continue_dialogue(self, query: models.Query):
        Dialogue._create_query(self.model._asdict() | query._asdict())
        self._history = None

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
    def model(self):
        return models.Query(self.question, self.answer, self.create_time)

    def __eq__(self, __o):
        if __o is not Query:
            return False
        return self.model == __o.model

    def __hash__(self):
        return hash(self.model)


class Graph:
    create: Executor = execute(
        "MATCH (u:User {username: $creator}) CREATE (u)-[:CREATE]->(g:Graph {gid: $gid, title: $title, "
        "creator: $creator, create_time: $create_time}) return g")
    """parameters: creator, gid, title, create_time"""

    get: Executor = execute("MATCH (:User {username: $username})-->(g:Graph) RETURN g")
    """parameters: username"""

    _detach_knowledge: Executor = execute("MATCH (g:Graph {creator: $creator, gid: $gid})-->(k:KNode) DETACH DELETE k")
    _detach: Executor = execute("MATCH (g:Graph {creator: $creator, gid: $gid}) DETACH DELETE g")

    _get_knowledge_node: Executor = execute("MATCH (g:Graph {creator: $creator, gid: $gid})-->(k:KNode) return k")
    _get_knowledge_relationship: Executor = execute(
        "MATCH (g:Graph {creator: $creator, gid: $gid})-->(:KNode)-[r]->(:KNode) return r")

    def __init__(self, graph: models.Graph | None):
        self._instance = None
        self._knowledge_nodes = None
        self._knowledge_relationships = None
        if graph is not None:
            self.creator = graph.creator
            self.gid = graph.gid
            self.title = graph.title
            self.create_time = graph.create_time
            self.edit_time = graph.edit_time

    @property
    def knowledge(self):
        if self._knowledge_nodes is not None and self._knowledge_relationships is not None:
            return self._knowledge_nodes.union(self._knowledge_relationships)
        records = Graph._get_knowledge_node(models.GraphBase(self.creator, self.gid)._asdict())
        k_nodes = {r["k"] for r in records}
        k_nodes = {models.KNode(node["label"], {k: v for k, v in node if k != "label"}) for node in k_nodes}
        self._knowledge_nodes = k_nodes

        records = Graph._get_knowledge_relationship(models.GraphBase(self.creator, self.gid)._asdict())
        k_rels = {r["r"] for r in records}
        k_rels = {models.KRelationship(rel["label"], {k: v for k, v in rel if k != "label"}) for rel in k_rels}
        self._knowledge_relationships = k_rels

        return self.knowledge

    def detach(self):
        Graph._detach_knowledge(models.GraphBase(self.creator, self.gid)._asdict())
        Graph._detach(models.GraphBase(self.creator, self.gid)._asdict())
