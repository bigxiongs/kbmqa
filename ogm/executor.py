from collections.abc import Generator
from typing import Callable

from database.session import execute


class User:
    get = execute("MATCH (u:User {username: $username}) RETURN u")
    """parameters: username"""

    create: Callable[[dict], Generator[tuple[dict]]] = execute(
        "CREATE (u:User {username: $username, password: $password, telephone: $telephone, "
        "email: $email, profile: $profile, create_time: $create_time}) RETURN u")
    """parameters: username, password, telephone, email, profile, create_time"""

    set: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (u:User {username: $username}) SET u.username = $new_name RETURN u")
    """parameters: username, new_name"""

    detach: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (u:User {username: $username}) DETACH DELETE u")
    """parameters: username"""


class Dialogue:
    create: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (u:User {username: $creator}) CREATE (u)-[:CREATE]->(d:Dialogue {did: $did, title: $title, "
        "creator: $creator}) return d")
    """parameters: creator, did, title"""

    get: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (:User {username: $username})-->(d:Dialogue) RETURN d")
    """parameters: username"""

    detach: Callable[[dict], Generator[None]] = execute(
        "MATCH (d:Dialogue {did: $did}) DETACH DELETE d")
    """parameters: did"""


class Query:
    create: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (d:Dialogue {did: $did, creator: $creator}) "
        "CREATE (d)-[:CONTAIN]->(q:Query {question: $question, answer: $answer, create_time: $create_time})"
        "RETURN q")
    """parameters: did, creator, question, answer, create_time"""

    get: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (d:Dialogue {did: $did})-->(q:Query) RETURN q")
    """parameters: did"""

    detach: Callable[[dict], Generator[None]] = execute(
        "MATCH (:Dialogue {did: $did})-->(q:Query) DETACH DELETE q")
    """parameters: did"""


class Graph:
    create: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (u:User {username: $creator}) CREATE (u)-[:CREATE]->(g:Graph {gid: $gid, title: $title, "
        "creator: $creator, create_time: $create_time}) return g")
    """parameters: creator, gid, title, create_time"""

    get: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (:User {username: $username})-->(g:Graph) RETURN g")
    """parameters: username"""

    detach: Callable[[dict], Generator[None]] = execute(
        "MATCH (g:Graph {gid: $gid}) DETACH DELETE g")
    """parameters: gid"""
