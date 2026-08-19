from database.connection import Database


db = Database()

queries = [
    """
    CREATE CONSTRAINT candidate_id_unique IF NOT EXISTS
    FOR (c:Candidate)
    REQUIRE c.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT skill_id_unique IF NOT EXISTS
    FOR (s:Skill)
    REQUIRE s.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT project_id_unique IF NOT EXISTS
    FOR (p:Project)
    REQUIRE p.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT company_id_unique IF NOT EXISTS
    FOR (c:Company)
    REQUIRE c.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT role_id_unique IF NOT EXISTS
    FOR (r:Role)
    REQUIRE r.id IS UNIQUE
    """
]


for query in queries:
    db.query(query)


db.close()

print("Database schema created successfully.")