from collections.abc import Generator
from typing import Callable, Any

from neo4j import GraphDatabase, Record

URI = "neo4j://localhost"
AUTH = ("rene", "00000000")
WRITE_KEYWORDS = ["DELETE", "CREATE", "SET"]

Executor = Callable[[dict], list[Record]]


# session generator
def _session_generator(database: str) -> Generator:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        while True:
            yield driver.session(database=database)


session_generator = _session_generator("neo4j")


# executor
def execute(statement: str, converter: Callable[[Any], Any] = lambda _: _) -> Executor:
    def work_func(stmt: str):
        return lambda tx, parameters: list(tx.run(stmt, **parameters))

    def _execute(_statement: str, _params: dict):
        with next(session_generator) as session:
            records = session.execute_write(work_func(_statement), _params) \
                if any(word in _statement for word in WRITE_KEYWORDS) \
                else session.execute_read(work_func(_statement), _params)
            return converter(records)

    return lambda parameters: _execute(statement, parameters)

# converter
# def field_process(record: dict) -> dict:
#     for k, v in record.items():
#         if type(v) is Date or type(v) is DateTime:
#             record[k] = v.to_native()
#         elif type(v) is dict:
#             record[k] = field_process(record[k])
#     return record
#
#
# def filter_rel(entity: Node | Relationship) -> dict:
#     if type(entity).__name__ == 'Node':
#         return {}
#     return {"start_node": entity_process(entity.start_node), "end_node": entity_process(entity.end_node)}
#
#
# def _entity_process(field_process, entity: Node | Relationship) -> dict:
#     """
#     process a single entity, convert it to a dict deeply (relationship-connected nodes are also be processed)
#     :param field_process: field_process
#     :param entity: the entity to be processed
#     :return: a dict represent the entity
#     """
#     return {"type": type(entity).__name__, **field_process(dict(entity)), **filter_rel(entity)}
#
#
# def entity_process(entity: Node | Relationship):
#     return _entity_process(field_process, entity)
#
#
# def records2tuple(records: list[Record]) -> Generator[tuple]:
#     yield from map(lambda record: tuple(map(entity_process, record)), records)
