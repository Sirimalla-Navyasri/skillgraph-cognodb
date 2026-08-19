from database.connection import Database


db = Database()


candidates = [
    {
        "id": "C001",
        "name": "Ananya Rao",
        "title": "Data Engineer",
        "location": "Hyderabad",
        "experience": 3
    },
    {
        "id": "C002",
        "name": "Rahul Sharma",
        "title": "Backend Developer",
        "location": "Bengaluru",
        "experience": 4
    },
    {
        "id": "C003",
        "name": "Priya Nair",
        "title": "ML Engineer",
        "location": "Chennai",
        "experience": 3
    },
    {
        "id": "C004",
        "name": "Arjun Mehta",
        "title": "Data Analyst",
        "location": "Mumbai",
        "experience": 2
    },
    {
        "id": "C005",
        "name": "Sneha Reddy",
        "title": "Full Stack Developer",
        "location": "Hyderabad",
        "experience": 4
    }
]


skills = [
    {"id": "S001", "name": "Python", "category": "Programming"},
    {"id": "S002", "name": "SQL", "category": "Database"},
    {"id": "S003", "name": "PostgreSQL", "category": "Database"},
    {"id": "S004", "name": "Pandas", "category": "Data"},
    {"id": "S005", "name": "NumPy", "category": "Data"},
    {"id": "S006", "name": "Machine Learning", "category": "AI"},
    {"id": "S007", "name": "Docker", "category": "DevOps"},
    {"id": "S008", "name": "AWS", "category": "Cloud"},
    {"id": "S009", "name": "Java", "category": "Programming"},
    {"id": "S010", "name": "Spring Boot", "category": "Backend"},
    {"id": "S011", "name": "React", "category": "Frontend"},
    {"id": "S012", "name": "JavaScript", "category": "Programming"},
    {"id": "S013", "name": "FastAPI", "category": "Backend"},
    {"id": "S014", "name": "ETL", "category": "Data Engineering"},
    {"id": "S015", "name": "Power BI", "category": "Analytics"}
]


projects = [
    {
        "id": "P001",
        "name": "Fraud Detection Platform",
        "description": "Machine learning platform for detecting suspicious transactions"
    },
    {
        "id": "P002",
        "name": "Sales Analytics Dashboard",
        "description": "Interactive sales analytics and reporting platform"
    },
    {
        "id": "P003",
        "name": "ETL Data Pipeline",
        "description": "Automated data ingestion and transformation pipeline"
    },
    {
        "id": "P004",
        "name": "Recommendation Engine",
        "description": "Personalized recommendation system"
    },
    {
        "id": "P005",
        "name": "Customer Management Platform",
        "description": "Customer relationship management application"
    }
]


companies = [
    {
        "id": "CO001",
        "name": "TechNova",
        "industry": "Technology"
    },
    {
        "id": "CO002",
        "name": "DataSphere",
        "industry": "Analytics"
    },
    {
        "id": "CO003",
        "name": "CloudWorks",
        "industry": "Cloud"
    },
    {
        "id": "CO004",
        "name": "FinEdge",
        "industry": "FinTech"
    },
    {
        "id": "CO005",
        "name": "RetailHub",
        "industry": "Retail"
    }
]


roles = [
    {"id": "R001", "title": "Data Engineer"},
    {"id": "R002", "title": "Backend Developer"},
    {"id": "R003", "title": "ML Engineer"},
    {"id": "R004", "title": "Data Analyst"},
    {"id": "R005", "title": "Full Stack Developer"}
]
db.query(
    """
    UNWIND $candidates AS candidate
    MERGE (c:Candidate {id: candidate.id})
    SET c.name = candidate.name,
        c.title = candidate.title,
        c.location = candidate.location,
        c.experience = candidate.experience
    """,
    {"candidates": candidates}
)


db.query(
    """
    UNWIND $skills AS skill
    MERGE (s:Skill {id: skill.id})
    SET s.name = skill.name,
        s.category = skill.category
    """,
    {"skills": skills}
)


db.query(
    """
    UNWIND $projects AS project
    MERGE (p:Project {id: project.id})
    SET p.name = project.name,
        p.description = project.description
    """,
    {"projects": projects}
)


db.query(
    """
    UNWIND $companies AS company
    MERGE (c:Company {id: company.id})
    SET c.name = company.name,
        c.industry = company.industry
    """,
    {"companies": companies}
)


db.query(
    """
    UNWIND $roles AS role
    MERGE (r:Role {id: role.id})
    SET r.title = role.title
    """,
    {"roles": roles}
)
candidate_skills = [
    ("C001", "S001"),
    ("C001", "S002"),
    ("C001", "S003"),
    ("C001", "S004"),
    ("C001", "S014"),

    ("C002", "S001"),
    ("C002", "S002"),
    ("C002", "S009"),
    ("C002", "S010"),
    ("C002", "S007"),

    ("C003", "S001"),
    ("C003", "S004"),
    ("C003", "S005"),
    ("C003", "S006"),
    ("C003", "S008"),

    ("C004", "S002"),
    ("C004", "S004"),
    ("C004", "S015"),

    ("C005", "S001"),
    ("C005", "S011"),
    ("C005", "S012"),
    ("C005", "S013")
]
db.query(
    """
    UNWIND $relationships AS rel

    MATCH (candidate:Candidate {id: rel[0]})
    MATCH (skill:Skill {id: rel[1]})

    MERGE (candidate)-[:HAS_SKILL]->(skill)
    """,
    {"relationships": candidate_skills}
)
candidate_projects = [
    ("C001", "P003"),
    ("C001", "P002"),

    ("C002", "P005"),
    ("C002", "P003"),

    ("C003", "P001"),
    ("C003", "P004"),

    ("C004", "P002"),

    ("C005", "P005")
]


db.query(
    """
    UNWIND $relationships AS rel

    MATCH (candidate:Candidate {id: rel[0]})
    MATCH (project:Project {id: rel[1]})

    MERGE (candidate)-[:WORKED_ON]->(project)
    """,
    {"relationships": candidate_projects}
)
project_skills = [
    ("P001", "S001"),
    ("P001", "S006"),
    ("P001", "S002"),

    ("P002", "S002"),
    ("P002", "S004"),
    ("P002", "S015"),

    ("P003", "S001"),
    ("P003", "S002"),
    ("P003", "S003"),
    ("P003", "S014"),

    ("P004", "S001"),
    ("P004", "S006"),
    ("P004", "S005"),

    ("P005", "S001"),
    ("P005", "S012"),
    ("P005", "S011")
]


db.query(
    """
    UNWIND $relationships AS rel

    MATCH (project:Project {id: rel[0]})
    MATCH (skill:Skill {id: rel[1]})

    MERGE (project)-[:USES_SKILL]->(skill)
    """,
    {"relationships": project_skills}
)
candidate_companies = [
    ("C001", "CO002"),
    ("C002", "CO001"),
    ("C003", "CO004"),
    ("C004", "CO005"),
    ("C005", "CO003")
]


db.query(
    """
    UNWIND $relationships AS rel

    MATCH (candidate:Candidate {id: rel[0]})
    MATCH (company:Company {id: rel[1]})

    MERGE (candidate)-[:WORKED_AT]->(company)
    """,
    {"relationships": candidate_companies}
)
candidate_roles = [
    ("C001", "R001"),
    ("C002", "R002"),
    ("C003", "R003"),
    ("C004", "R004"),
    ("C005", "R005")
]


db.query(
    """
    UNWIND $relationships AS rel

    MATCH (candidate:Candidate {id: rel[0]})
    MATCH (role:Role {id: rel[1]})

    MERGE (candidate)-[:HELD_ROLE]->(role)
    """,
    {"relationships": candidate_roles}
)
related_skills = [
    ("S001", "S013"),
    ("S001", "S004"),
    ("S001", "S005"),

    ("S002", "S003"),
    ("S002", "S014"),

    ("S006", "S005"),
    ("S008", "S007"),

    ("S011", "S012"),
    ("S012", "S013")
]


db.query(
    """
    UNWIND $relationships AS rel

    MATCH (skill1:Skill {id: rel[0]})
    MATCH (skill2:Skill {id: rel[1]})

    MERGE (skill1)-[:RELATED_TO]->(skill2)
    """,
    {"relationships": related_skills}
)
role_skills = [
    ("R001", "S001"),
    ("R001", "S002"),
    ("R001", "S003"),
    ("R001", "S014"),

    ("R002", "S001"),
    ("R002", "S009"),
    ("R002", "S010"),

    ("R003", "S001"),
    ("R003", "S006"),
    ("R003", "S005"),

    ("R004", "S002"),
    ("R004", "S004"),
    ("R004", "S015"),

    ("R005", "S011"),
    ("R005", "S012"),
    ("R005", "S013")
]


db.query(
    """
    UNWIND $relationships AS rel

    MATCH (role:Role {id: rel[0]})
    MATCH (skill:Skill {id: rel[1]})

    MERGE (role)-[:REQUIRES]->(skill)
    """,
    {"relationships": role_skills}
)
db.close()

print("Seed data loaded successfully!")