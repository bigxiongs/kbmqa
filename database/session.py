from neo4j import GraphDatabase

URI = "neo4j://localhost"
AUTH = ("rene", "00000000")
WRITE_KEYWORDS = ["DELETE", "CREATE", "SET"]


def session_generator():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        while True:
            yield driver.session(database="neo4j")


session_generator = session_generator()


def work_func(stmt):
    return lambda tx, parameters: list(tx.run(stmt, **parameters))


def execute(stmt: str, parameters):
    if any(word in stmt for word in WRITE_KEYWORDS):
        with next(session_generator) as session:
            return session.execute_write(work_func(stmt), parameters)
    with next(session_generator) as session:
        return session.execute_read(work_func(stmt), parameters)
