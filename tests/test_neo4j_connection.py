from neo4j import GraphDatabase


URI = "neo4j://localhost"
AUTH = ("rene", "00000000")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    records, summay, keys = driver.execute_query("MERGE (u:User {username: 'rene'}) RETURN u", database_="neo4j")
    print(records, summay, keys)