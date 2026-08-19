SkillGraph — Graph-Based Candidate & Career Explorer

A graph-powered web application for exploring relationships between candidates, skills, projects, companies, and career roles.

Built as part of the Wexa AI CognoDB Take-Home Assignment.

---

Live Demo

Hosted Application: https://skillgraph-cognodb-5r66.onrender.com

GitHub Repository: https://github.com/Sirimalla-Navyasri/skillgraph-cognodb.git

Screen Recording: https://drive.google.com/file/d/1bBY307x_tJ0wEMX797bbD4URxKfZ4Fpc/view?usp=drivesdk

---

Overview

SkillGraph is a graph-based candidate exploration application that helps users discover relationships between people, skills, projects, companies, and career roles.

Instead of treating candidate information as isolated records, SkillGraph models the connections between these entities.

Users can:

- Browse candidates
- Search candidates by name or role
- View candidate skills, projects, companies, and roles
- Find candidates with similar skills
- Find candidates suitable for a particular career role
- Explore related career paths
- Traverse multi-hop relationships in the graph

The application is backed by CognoDB and communicates with it using the official Neo4j Python driver over the Bolt protocol.

---

Why a Graph Database?

The central questions in SkillGraph are about relationships and paths, rather than isolated records.

A traditional relational database could represent the same information using tables such as:

candidates
skills
candidate_skills
projects
candidate_projects
project_skills
companies
candidate_companies
roles
role_skills
skill_relationships

However, relationship-heavy questions would require multiple joins and junction tables.

For example:

«Find candidates who have skills related to the skills required for a Data Engineer role and who have worked on projects using those skills.»

In a relational schema, this requires several joins across mapping tables.

In the graph model, the same problem can be expressed as a traversal:

Candidate
    |
 HAS_SKILL
    |
  Skill
    |
RELATED_TO
    |
  Skill
    |
 REQUIRED_BY
    |
  Role

Another example:

Candidate
    |
WORKED_ON
    |
 Project
    |
USES_SKILL
    |
  Skill

These connections are first-class entities in the graph.

This makes graph traversal natural and makes the application easy to extend with additional relationships.

---

Key Features

1. Candidate Explorer

Users can browse all candidates and search by:

- Candidate name
- Job title

---

2. Candidate Profile

Each candidate profile displays:

- Name
- Current title
- Location
- Years of experience
- Skills
- Projects
- Companies
- Career roles

---

3. Similar Candidates

SkillGraph can identify candidates who share skills with another candidate.

The graph traversal is:

Candidate A
     |
 HAS_SKILL
     |
   Skill
     |
 HAS_SKILL
     |
Candidate B

The application returns candidates with the highest number of shared skills.

---

4. Role-Based Candidate Matching

Users can select a career role and find candidates who have the skills required for that role.

Example:

Data Engineer
      |
  REQUIRES
      |
    Python
      |
  HAS_SKILL
      |
 Candidate

The result also shows the skills matching the selected role.

---

5. Career Path Exploration

Users can explore other roles that have overlapping skills with their current role.

For example:

Data Analyst
      |
 Shared Skills
      |
Data Engineer
      |
 Shared Skills
      |
ML Engineer

---

6. Multi-Hop Graph Traversal

The application contains Cypher queries that traverse multiple relationships.

Example:

Candidate
    ↓
Project
    ↓
Skill

This demonstrates a two-hop graph traversal.

---

Technology Stack

Layer| Technology
Database| CognoDB
Query Language| openCypher
Protocol| Bolt
Database Driver| Official Neo4j Python Driver
Backend| Flask
Frontend| HTML, CSS, JavaScript
Templates| Jinja2
Configuration| Python dotenv
Production Server| Gunicorn
Hosting| Render
Version Control| Git / GitHub

---

Architecture

┌─────────────────────────────┐
│          User               │
│       Web Browser           │
└──────────────┬──────────────┘
               │
               │ HTTP
               ▼
┌─────────────────────────────┐
│       Flask Application     │
│                             │
│  Routes                     │
│  API Endpoints              │
│  Error Handling             │
│  Database Layer             │
└──────────────┬──────────────┘
               │
               │ Neo4j Python Driver
               │ Bolt
               ▼
┌─────────────────────────────┐
│          CognoDB            │
│                             │
│ Candidate                   │
│ Skill                       │
│ Project                     │
│ Company                     │
│ Role                        │
│ Location                    │
└─────────────────────────────┘

---

Graph Data Model

Nodes

Candidate

(:Candidate {
    id,
    name,
    title,
    location,
    experience
})

Skill

(:Skill {
    id,
    name,
    category
})

Project

(:Project {
    id,
    name,
    description
})

Company

(:Company {
    id,
    name,
    industry
})

Role

(:Role {
    id,
    title
})

Location

(:Location {
    id,
    name
})

---

Relationships

(:Candidate)-[:HAS_SKILL]->(:Skill)

(:Candidate)-[:WORKED_ON]->(:Project)

(:Candidate)-[:WORKED_AT]->(:Company)

(:Candidate)-[:HELD_ROLE]->(:Role)

(:Candidate)-[:LOCATED_IN]->(:Location)

(:Project)-[:USES_SKILL]->(:Skill)

(:Skill)-[:RELATED_TO]->(:Skill)

(:Role)-[:REQUIRES]->(:Skill)

(:Company)-[:HIRES_FOR]->(:Role)

(:Company)-[:LOCATED_IN]->(:Location)

(:Role)-[:SIMILAR_TO]->(:Role)

---

Graph Diagram

graph TD

    Candidate -->|HAS_SKILL| Skill
    Candidate -->|WORKED_ON| Project
    Candidate -->|WORKED_AT| Company
    Candidate -->|HELD_ROLE| Role
    Candidate -->|LOCATED_IN| Location

    Project -->|USES_SKILL| Skill

    Skill -->|RELATED_TO| Skill

    Role -->|REQUIRES| Skill

    Company -->|HIRES_FOR| Role
    Company -->|LOCATED_IN| Location

    Role -->|SIMILAR_TO| Role

---

Example Graph

                 ┌─────────────┐
                 │   Company   │
                 └──────┬──────┘
                        │
                    WORKED_AT
                        │
                        ▼
                 ┌─────────────┐
                 │  Candidate  │
                 └──────┬──────┘
                        │
             ┌──────────┼──────────┐
             │          │          │
         HAS_SKILL   WORKED_ON  HELD_ROLE
             │          │          │
             ▼          ▼          ▼
          ┌──────┐   ┌────────┐  ┌──────┐
          │Skill │   │Project │  │ Role │
          └──┬───┘   └───┬────┘  └──┬───┘
             │           │           │
        RELATED_TO   USES_SKILL   REQUIRES
             │           │           │
             └───────────┴───────────┘

---

Project Structure

skillgraph-cognodb/
│
├── database/
│   ├── connection.py
│   ├── schema.py
│   ├── seed.py
│   └── queries.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── candidates.html
│   ├── candidate.html
│   ├── skills.html
│   └── careers.html
│
├── screenshots/
│   ├── dashboard.png
│   ├── candidates.png
│   ├── candidate-detail.png
│   ├── recommendations.png
│   └── career-explorer.png
│
├── app.py
├── test_connection.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

---

Data

The project uses realistic seed data designed to demonstrate graph relationships.

The seed dataset contains entities such as:

- Candidates
- Skills
- Projects
- Companies
- Roles
- Locations

The seed script is included in:

database/seed.py

The script uses parameterized Cypher queries and "UNWIND" to load batches of data efficiently.

The seed data is intentionally small enough to run comfortably on the CognoDB free tier while still providing enough relationships to demonstrate graph traversal.

---

Main Cypher Queries

1. Get All Candidates

MATCH (c:Candidate)
RETURN
    c.id AS id,
    c.name AS name,
    c.title AS title,
    c.location AS location,
    c.experience AS experience
ORDER BY c.name

This query retrieves all candidate nodes.

---

2. Get Candidate Details

MATCH (c:Candidate {id: $candidate_id})

OPTIONAL MATCH (c)-[:HAS_SKILL]->(skill:Skill)

OPTIONAL MATCH (c)-[:WORKED_ON]->(project:Project)

OPTIONAL MATCH (c)-[:WORKED_AT]->(company:Company)

OPTIONAL MATCH (c)-[:HELD_ROLE]->(role:Role)

RETURN
    c.id AS id,
    c.name AS name,
    c.title AS title,
    c.location AS location,
    c.experience AS experience,
    collect(DISTINCT skill.name) AS skills,
    collect(DISTINCT project.name) AS projects,
    collect(DISTINCT company.name) AS companies,
    collect(DISTINCT role.title) AS roles

The query uses the candidate ID as a parameter.

---

3. Search Candidates

MATCH (c:Candidate)

WHERE
    toLower(c.name) CONTAINS toLower($search)
    OR
    toLower(c.title) CONTAINS toLower($search)

RETURN
    c.id AS id,
    c.name AS name,
    c.title AS title,
    c.location AS location,
    c.experience AS experience

ORDER BY c.name

---

4. Candidates by Skill

MATCH (c:Candidate)-[:HAS_SKILL]->(s:Skill)

WHERE toLower(s.name) = toLower($skill)

RETURN
    c.id AS id,
    c.name AS name,
    c.title AS title,
    c.location AS location

ORDER BY c.name

---

Multi-Hop Traversal

One of the required graph queries is:

MATCH (c:Candidate)-[:WORKED_ON]->(p:Project)
      -[:USES_SKILL]->(s:Skill)

RETURN
    c.name AS candidate,
    p.name AS project,
    s.name AS skill

ORDER BY candidate

This performs a two-hop traversal:

Candidate
    |
WORKED_ON
    |
Project
    |
USES_SKILL
    |
Skill

This demonstrates how the application can navigate through multiple connected entities.

---

Similar Candidates Query

The application finds candidates who share skills.

MATCH (c1:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(s:Skill)
      <-[:HAS_SKILL]-(c2:Candidate)

WHERE c1 <> c2

RETURN
    c2.id AS id,
    c2.name AS name,
    c2.title AS title,
    count(s) AS shared_skills,
    collect(s.name) AS skills

ORDER BY shared_skills DESC

LIMIT 5

The graph path is:

Candidate A
     ↓
   Skill
     ↑
Candidate B

---

Role-Based Candidate Matching

MATCH (c:Candidate)-[:HAS_SKILL]->(s:Skill)
      <-[:REQUIRES]-(r:Role)

WHERE r.id = $role_id

RETURN
    c.id AS id,
    c.name AS name,
    c.title AS title,
    collect(s.name) AS matching_skills,
    count(s) AS skill_match_count

ORDER BY skill_match_count DESC

This allows the application to identify candidates based on their connection to the skills required by a role.

---

Related Skill Traversal

The application can also traverse relationships between related skills.

Example:

MATCH (candidate:Candidate)
      -[:HAS_SKILL]->(candidateSkill:Skill)

OPTIONAL MATCH path =
    (candidateSkill)-[:RELATED_TO*1..2]->(requiredSkill:Skill)

RETURN
    candidate.name AS candidate,
    candidateSkill.name AS candidate_skill,
    requiredSkill.name AS related_skill

The "*1..2" relationship pattern allows traversal across one or two "RELATED_TO" relationships.

---

Parameterized Queries

All user-controlled values are passed as Cypher parameters.

Example:

db.query(
    GET_CANDIDATE,
    {
        "candidate_id": candidate_id
    }
)

The Cypher query uses:

$candidate_id

instead of constructing a query using string concatenation.

This keeps the query structure separate from user input and avoids unsafe Cypher construction.

---

Database Connection

Database credentials are loaded from environment variables.

Required variables:

COGNODB_URI=bolt+s://your-instance.databases.cognodb.cloud
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=your-password
COGNODB_DATABASE=neo4j

The actual ".env" file is intentionally excluded from Git.

Only ".env.example" is included in the repository.

---

Setup Instructions

1. Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL

Move into the project:

cd skillgraph-cognodb

---

2. Create a Virtual Environment

Windows:

python -m venv venv

Activate:

venv\Scripts\activate

macOS/Linux:

python3 -m venv venv

Activate:

source venv/bin/activate

---

3. Install Dependencies

pip install -r requirements.txt

---

4. Create a CognoDB Instance

Create a CognoDB Cloud account and provision a free instance.

Use the connection details provided by CognoDB.

The application expects a Bolt URI in the following format:

bolt+s://<instance-id>.databases.cognodb.cloud

---

5. Configure Environment Variables

Create a file named:

.env

Add:

COGNODB_URI=bolt+s://YOUR_INSTANCE_ID.databases.cognodb.cloud
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=YOUR_PASSWORD
COGNODB_DATABASE=neo4j

Replace the placeholder values with the credentials from your CognoDB instance.

Do not commit ".env" to GitHub.

---

6. Test the Database Connection

Run:

python test_connection.py

Expected output:

Connected to CognoDB successfully!

---

7. Create the Database Schema

Run:

python database/schema.py

Expected output:

Database schema created successfully.

---

8. Load Seed Data

Run:

python database/seed.py

Expected output:

Seed data loaded successfully!

The seed script can be safely rerun because it uses "MERGE" for nodes and relationships.

---

9. Start the Application

Run:

python app.py

Open the application in a browser:

http://127.0.0.1:5000

---

Health Check

The application provides:

/health

Example:

http://127.0.0.1:5000/health

When the database is reachable, the endpoint returns:

{
    "status": "healthy",
    "database": "connected"
}

If the database is unavailable, the application returns an appropriate error response rather than exposing an internal stack trace.

---

Error Handling

The application handles database failures gracefully.

Examples include:

- Database unavailable
- Candidate not found
- Empty search results
- Failed API request

Instead of displaying a Python traceback, the UI displays a user-friendly message.

Example:

Unable to connect to the graph database.

For empty searches:

No candidates found.

Try another search.

For loading operations:

Finding similar candidates...

---

UI / UX

The application was designed with the following principles:

- Simple navigation
- Responsive layout
- Clear typography
- Consistent cards and tags
- Search functionality
- Loading states
- Empty states
- Error states
- Clear candidate profiles
- Simple relationship-driven interactions

The goal is to make the graph-backed functionality accessible to a non-technical user.

---

Screenshots

Dashboard

"Dashboard" (screenshots/dashboard.png)

The dashboard provides an overview of SkillGraph and directs users to candidate exploration.

---

Candidate Explorer

"Candidates" (screenshots/candidates.png)

Users can search and browse candidates.

---

Candidate Details

"Candidate Details" (screenshots/candidate-detail.png)

The candidate profile displays skills, projects, companies, and roles.

---

Similar Candidates

"Recommendations" (screenshots/recommendations.png)

The recommendation feature finds candidates connected through shared skills.

---

Career Explorer

"Career Explorer" (screenshots/career-explorer.png)

The career explorer uses role and skill relationships to identify related career paths.

---

Deployment

The application is designed to run on a free web hosting platform such as Render.

Production start command:

gunicorn app:app

Build command:

pip install -r requirements.txt

Production environment variables:

COGNODB_URI
COGNODB_USERNAME
COGNODB_PASSWORD
COGNODB_DATABASE

Secrets are configured through the hosting provider's environment-variable settings rather than committed to the repository.

---

Security Considerations

The application follows several basic security practices:

1. Database credentials are stored in environment variables.
2. ".env" is excluded from Git.
3. Cypher queries use parameters.
4. User input is not directly concatenated into Cypher.
5. Database errors are handled without exposing internal details.
6. The production database password is not included in source code.

---

Engineering Decisions

Why Flask?

Flask was selected because the application is relatively small and benefits from a lightweight backend.

It provides:

- Simple routing
- Easy template rendering
- Straightforward API endpoints
- Minimal project complexity

---

Why the Official Neo4j Python Driver?

CognoDB exposes an openCypher/Bolt interface compatible with the official Neo4j driver.

Using the official driver keeps the database access layer simple and avoids introducing an unnecessary custom SDK abstraction.

---

Why "UNWIND" in the Seed Script?

The seed script uses "UNWIND" to insert batches of records.

Instead of sending one database query for every node, multiple records can be passed as parameters and processed together.

---

Why "MERGE" in the Seed Script?

"MERGE" allows the seed script to be rerun without unintentionally creating duplicate nodes or relationships.

This makes database initialization easier during development and testing.

---

Example End-to-End Flow

A typical user interaction is:

User opens SkillGraph
        ↓
Dashboard
        ↓
Candidate Explorer
        ↓
Search for "Data"
        ↓
Open candidate
        ↓
View skills and projects
        ↓
Find Similar Candidates
        ↓
Flask API
        ↓
Parameterized Cypher
        ↓
CognoDB
        ↓
Graph traversal
        ↓
Similar candidates
        ↓
Display results

---

Future Improvements

Possible future enhancements include:

- Interactive graph visualization
- Authentication and user accounts
- Candidate comparison
- Advanced skill-gap analysis
- Job description matching
- Skill recommendation
- More sophisticated career-path scoring
- Candidate-to-job matching
- Pagination for larger datasets
- Caching for frequently used queries
- Automated data ingestion from external sources
- Graph analytics and ranking

---

Assignment Requirements Mapping

Wexa Requirement| Implementation
Graph database| CognoDB
Thoughtful graph model| Candidate, Skill, Project, Company, Role, Location
Typed relationships| "HAS_SKILL", "WORKED_ON", "WORKED_AT", "REQUIRES", etc.
Realistic seed data| "database/seed.py"
Seed script included| Yes
Multi-hop traversal| Candidate → Project → Skill
Relationally awkward query| Related skills / role matching
Official Neo4j driver| "neo4j" Python package
Parameterized Cypher| "$candidate_id", "$role_id", "$search", etc.
Functional web application| Flask
Non-technical UI| Candidate and career explorer
Loading state| Implemented
Empty state| Implemented
Error state| Implemented
Environment variables| ".env" / hosting environment
Secrets excluded| ".gitignore"
Database error handling| Flask exception handling
Graph diagram| Mermaid diagram
README documentation| This document
Hosted demo| YOUR_RENDER_DEMO_URL
Screen recording| YOUR_SCREEN_RECORDING_URL

---

Conclusion

SkillGraph demonstrates how a graph database can be used to solve a relationship-centric problem.

The application goes beyond storing candidate records by modeling connections between:

Candidates
    ↓
Skills
    ↓
Projects
    ↓
Companies
    ↓
Roles
    ↓
Locations

These relationships enable multi-hop traversal, candidate similarity, skill-based role matching, and career-path exploration.

The project is intentionally designed as a small, maintainable application that demonstrates graph modeling, Cypher querying, backend engineering, database integration, and user-focused UI/UX.

---

Author

Navyasri Sirimalla

GitHub: https://github.com/Sirimalla-Navyasri

Project Repository: https://github.com/Sirimalla-Navyasri/skillgraph-cognodb.git

Live Demo: https://skillgraph-cognodb-5r66.onrender.com