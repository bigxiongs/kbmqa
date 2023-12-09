from collections.abc import Generator
from typing import Callable

from database.session import execute, converter


class User:
    get: Callable[[dict], Generator[tuple[dict]]] = execute("MATCH (u:User {username: $username}) RETURN u", converter)
    """parameters: username"""

    create: Callable[[dict], Generator[tuple[dict]]] = execute(
        "CREATE (u:User {username: $username, password: $password, telephone: $telephone, "
        "email: $email, profile: $profile, create_time: $create_time}) RETURN u", converter)
    """parameters: username, password, telephone, email, profile, create_time"""

    set: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (u:User {username: $username}) SET u.username = $new_name RETURN u", converter)
    """parameters: username, new_name"""

    detach: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (u:User {username: $username}) DETACH DELETE u", converter)
    """parameters: username"""


class Dialogue:
    create: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (u:User {username: $creator}) CREATE (u)-[:CREATE]->(d:Dialogue {did: $did, title: $title, "
        "creator: $creator}) return d", converter)
    """parameters: creator, did, title"""

    get: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (:User {username: $username})-->(d:Dialogue) RETURN d", converter)
    """parameters: username"""

    detach: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (d:Dialogue {did: $did}) DETACH DELETE d", converter)
    """parameters: did"""


class Query:
    create: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (d:Dialogue {did: $did, creator: $creator}) "
        "CREATE (d)-[:CONTAIN]->(q:Query {question: $question, answer: $answer, create_time: $create_time})"
        "RETURN q", converter)
    """parameters: did, creator, question, answer, create_time"""

    get: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (d:Dialogue {did: $did})-->(q:Query) RETURN q", converter)
    """parameters: did"""

    detach: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (:Dialogue {did: $did})-->(q:Query) DETACH DELETE q", converter)
    """parameters: did"""


class Graph:
    create: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (u:User {username: $creator}) CREATE (u)-[:CREATE]->(g:Graph {gid: $gid, title: $title, "
        "creator: $creator, create_time: $create_time}) return g", converter)
    """parameters: creator, gid, title, create_time"""

    get: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (:User {username: $username})-->(g:Graph) RETURN g", converter)
    """parameters: username"""

    detach: Callable[[dict], Generator[tuple[dict]]] = execute(
        "MATCH (g:Graph {gid: $gid}) DETACH DELETE g", converter)
    """parameters: gid"""
