from neo4j import GraphDatabase

URI = "neo4j://localhost"
AUTH = ("rene", "00000000")


def func(tx):
    result = tx.run("MATCH (u:User)-[r]->(d:Dialogue) RETURN u, r, d")
    record = result.single()
    print(record)
    return record


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        record = session.execute_write(func)
        ...
        print(record)
