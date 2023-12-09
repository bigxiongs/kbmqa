from collections.abc import Generator
from typing import Callable

from neo4j import Record

from database.session import execute, records_convert, field_convert


class User:
    converter: Callable[[list[Record]], Generator[dict]] = records_convert(
        'u', field_convert('create_time', lambda o: o.to_native()))

    get: Callable[[dict], Generator[dict]] = execute("MATCH (u:User {username: $username}) RETURN u", converter)
    """parameters: username"""
    create: Callable[[dict], Generator[dict]] = execute(
        "CREATE (u:User {username: $username, password: $password, telephone: $telephone, "
        "email: $email, profile: $profile, create_time: $create_time}) RETURN u",
        converter)
    """parameters: username, password, telephone, email, profile, create_time"""
    set: Callable[[dict], Generator[dict]] = execute(
        "MATCH (u:User {username: $username}) SET u.username = $new_name RETURN u", converter)
    """parameters: username, new_name"""
    detach: Callable[[dict], Generator[dict]] = execute(
        "MATCH (u:User {username: $username}) DETACH DELETE u", converter)
    """parameters: username"""


class Dialogue:
    converter: Callable[[list[Record]], Generator[dict]] = records_convert('d', lambda d: ...)

    create: Callable[[dict], Generator[dict]] = execute(
        "MATCH (u:User {username: $creator}) CREATE (u)-[:CREATE]->(d:Dialogue {did: $did, title: $title, "
        "creator: $creator}) return d", converter)
    """parameters: creator, did, title"""
    get: Callable[[dict], Generator[dict]] = execute(
        "MATCH (:User {username: $username})-->(d:Dialogue) RETURN d", converter)
    """parameters: username"""
    detach: Callable[[dict], Generator[dict]] = execute(
        "MATCH (d:Dialogue {did: $did}) DETACH DELETE d", converter
    )
    """parameters: did"""


class Query:
    converter: Callable[[list[Record]], Generator[dict]] = records_convert(
        'q', field_convert('create_time', lambda t: t.to_native()))

    create: Callable[[dict], Generator[dict]] = execute(
        "MATCH (d:Dialogue {did: $did, creator: $creator}) "
        "CREATE (d)-[:CONTAIN]->(q:Query {question: $question, answer: $answer, create_time: $create_time})"
        "RETURN q", converter)
    """parameters: did, creator, question, answer, create_time"""
    get: Callable[[dict], Generator[dict]] = execute(
        "MATCH (d:Dialogue {did: $did})-->(q:Query) RETURN q", converter)
    """parameters: did"""
    detach: Callable[[dict], Generator[dict]] = execute(
        "MATCH (:Dialogue {did: $did})-->(q:Query) DETACH DELETE q", converter
    )
    """parameters: did"""
