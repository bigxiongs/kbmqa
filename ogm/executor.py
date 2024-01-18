from database.session import execute, Executor

import database.tuples as models


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

    def __init__(self, user: models.UserBase | models.User | None):
        records = User._get(user._asdict()) if user is not None else []
        if isinstance(user, models.User):
            assert len(records) == 0, "user already exists"
            records = User._create(user._asdict())
        self._info = records

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
    def info(self) -> models.User | None:
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
        records = User._set_name({"username": self._info.username, "new_name": new_name})
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

    def detach(self):
        if self._info is not None:
            User._detach(models.UserBase(self.username)._asdict())
            return User(models.UserBase(self.username))
        assert False

    def __eq__(self, __o):
        if __o is not User:
            return False
        return self.info == __o.info

    def __hash__(self):
        return hash(self.info)


class Dialogue:
    create: Executor = execute(
        "MATCH (u:User {username: $creator}) CREATE (u)-[:CREATE]->(d:Dialogue {did: $did, title: $title, "
        "creator: $creator}) return d")
    """parameters: creator, did, title"""

    get: Executor = execute("MATCH (:User {username: $username})-->(d:Dialogue) RETURN d")
    """parameters: username"""

    detach: Executor = execute("MATCH (d:Dialogue {did: $did}) DETACH DELETE d")
    """parameters: did"""


class Query:
    create: Executor = execute(
        "MATCH (d:Dialogue {did: $did, creator: $creator}) "
        "CREATE (d)-[:CONTAIN]->(q:Query {question: $question, answer: $answer, create_time: $create_time})"
        "RETURN q")
    """parameters: did, creator, question, answer, create_time"""

    get: Executor = execute("MATCH (d:Dialogue {did: $did})-->(q:Query) RETURN q")
    """parameters: did"""

    detach: Executor = execute("MATCH (:Dialogue {did: $did})-->(q:Query) DETACH DELETE q")
    """parameters: did"""


class Graph:
    create: Executor = execute(
        "MATCH (u:User {username: $creator}) CREATE (u)-[:CREATE]->(g:Graph {gid: $gid, title: $title, "
        "creator: $creator, create_time: $create_time}) return g")
    """parameters: creator, gid, title, create_time"""

    get: Executor = execute("MATCH (:User {username: $username})-->(g:Graph) RETURN g")
    """parameters: username"""

    detach: Executor = execute("MATCH (g:Graph {gid: $gid}) DETACH DELETE g")
    """parameters: gid"""
