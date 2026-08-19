import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


class Database:

    def __init__(self):
        self.uri = os.getenv("COGNODB_URI")
        self.username = os.getenv("COGNODB_USERNAME")
        self.password = os.getenv("COGNODB_PASSWORD")
        self.database = os.getenv("COGNODB_DATABASE")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def query(self, query, parameters=None):
        with self.driver.session(database=self.database) as session:
            result = session.run(query, parameters or {})
            return result.data()

    def verify(self):
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()