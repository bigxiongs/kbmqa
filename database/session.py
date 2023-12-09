from collections.abc import Generator
from typing import Callable

from neo4j.time import Date, DateTime
from functoolz import curry
from neo4j import GraphDatabase, Record
from neo4j.graph import Node, Relationship

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
def execute(stmt: str, convert: Callable[[list[Record]], Generator[dict]], parameters: dict) -> Generator[dict]:
    if any(word in stmt for word in WRITE_KEYWORDS):
        with next(session_generator) as session:
            return convert(session.execute_write(work_func(stmt), parameters))
    with next(session_generator) as session:
        return convert(session.execute_read(work_func(stmt), parameters))


@curry
def records_convert(func: Callable[[Record], tuple], records: list[Record]) -> tuple[dict]:
    for record in records:
        yield func(record)


def field_process(record: dict) -> dict:
    for k, v in record.items():
        if type(v) is Date or type(v) is DateTime:
            record[k] = v.to_native()
        elif type(v) is dict:
            record[k] = field_process(record[k])
    return record


def record_process(record: Record) -> Callable[[Callable[[Node | Relationship], dict]], tuple]:
    return lambda func: tuple(map(func, record))


def filter_rel(entity: Node | Relationship) -> dict:
    if type(entity).__name__ == 'Node':
        return {}
    return {"start_node": entity_process(entity.start_node), "end_node": entity_process(entity.end_node)}


@curry
def entity_process(func, entity: Node | Relationship) -> dict:
    return {"type": type(entity).__name__, **func(dict(entity)), **filter_rel(entity)}


def process_func(record: Record) -> tuple:
    return record_process(record)(entity_process(field_process))


converter = records_convert(process_func)

if __name__ == '__main__':
    ...
