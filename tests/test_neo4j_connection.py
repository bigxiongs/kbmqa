from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://localhost"
AUTH = ("neo4j", "00000000")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()