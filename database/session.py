from collections.abc import Iterable, Generator
from typing import Callable, Any

from neo4j import GraphDatabase, Record
from functoolz import curry

URI = "neo4j://localhost"
AUTH = ("rene", "00000000")
WRITE_KEYWORDS = ["DELETE", "CREATE", "SET"]


def session_generator():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        while True:
            yield driver.session(database="neo4j")


session_generator = session_generator()


def work_func(stmt: str):
    return lambda tx, parameters: list(tx.run(stmt, **parameters))


@curry
def execute(stmt: str, converter: Callable[[list[Record]], Generator[dict]], parameters: dict) -> Generator[dict]:
    if any(word in stmt for word in WRITE_KEYWORDS):
        with next(session_generator) as session:
            return converter(session.execute_write(work_func(stmt), parameters))
    with next(session_generator) as session:
        return converter(session.execute_read(work_func(stmt), parameters))


@curry
def records_convert(identifier: str, func: Callable[[dict], None], records: list[Record]) -> Generator[dict]:
    for record in records:
        record = record[identifier]
        record = dict(record)
        func(record)
        yield record


@curry
def field_convert(field: str, func: Callable[[Any], Any], record: dict) -> None:
    record[field] = func(record[field])
