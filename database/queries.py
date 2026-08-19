# ==================================================
# GET ALL CANDIDATES
# ==================================================

GET_CANDIDATES = """
MATCH (c:Candidate)

RETURN
    c.id AS id,
    c.name AS name,
    c.title AS title,
    c.location AS location,
    c.experience AS experience

ORDER BY c.name
"""


# ==================================================
# GET SINGLE CANDIDATE
# ==================================================

GET_CANDIDATE = """
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
"""


# ==================================================
# SEARCH CANDIDATES
# ==================================================

SEARCH_CANDIDATES = """
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
"""


# ==================================================
# CANDIDATES BY SKILL
# ==================================================

CANDIDATES_BY_SKILL = """
MATCH (c:Candidate)-[:HAS_SKILL]->(s:Skill)

WHERE toLower(s.name) = toLower($skill)

RETURN
    c.id AS id,
    c.name AS name,
    c.title AS title,
    c.location AS location

ORDER BY c.name
"""


# ==================================================
# PROJECT SKILL USAGE
# ==================================================

PROJECT_SKILL_USAGE = """
MATCH (c:Candidate)-[:WORKED_ON]->(p:Project)
      -[:USES_SKILL]->(s:Skill)

RETURN
    c.name AS candidate,
    p.name AS project,
    s.name AS skill

ORDER BY candidate
"""


# ==================================================
# CANDIDATES FOR ROLE
# ==================================================

CANDIDATES_FOR_ROLE = """
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
"""


# ==================================================
# SMART ROLE MATCH
# ==================================================

SMART_ROLE_MATCH = """
MATCH (role:Role {id: $role_id})
      -[:REQUIRES]->(required:Skill)

MATCH (candidate:Candidate)
      -[:HAS_SKILL]->(candidate_skill:Skill)

OPTIONAL MATCH path =
    (candidate_skill)-[:RELATED_TO*1..2]->(required)

WITH
    candidate,
    required,
    candidate_skill,
    path

WITH
    candidate,
    collect(
        DISTINCT CASE
            WHEN candidate_skill.id = required.id
            THEN required.name

            WHEN path IS NOT NULL
            THEN candidate_skill.name + " → " + required.name
        END
    ) AS matched_skills,

    count(path) AS related_matches

RETURN
    candidate.id AS id,
    candidate.name AS name,
    candidate.title AS title,
    matched_skills,
    related_matches

ORDER BY related_matches DESC

LIMIT 10
"""


# ==================================================
# SIMILAR CANDIDATES
# ==================================================

SIMILAR_CANDIDATES = """
MATCH (c1:Candidate {id: $candidate_id})
      -[:HAS_SKILL]->(s:Skill)
      <-[:HAS_SKILL]-(c2:Candidate)

WHERE c1 <> c2

RETURN
    c2.id AS id,
    c2.name AS name,
    c2.title AS title,
    count(s) AS shared_skills,
    collect(DISTINCT s.name) AS skills

ORDER BY shared_skills DESC

LIMIT 5
"""


# ==================================================
# CAREER PATH
# ==================================================

CAREER_PATH = """
MATCH (current:Role {id: $role_id})
      -[:REQUIRES]->(skill:Skill)

MATCH (next:Role)
      -[:REQUIRES]->(skill)

WHERE current <> next

RETURN
    next.id AS id,
    next.title AS title,
    collect(DISTINCT skill.name) AS shared_skills,
    count(DISTINCT skill) AS overlap

ORDER BY overlap DESC

LIMIT 10
"""


# ==================================================
# MULTI-HOP GRAPH TRAVERSAL
# ==================================================

MULTI_HOP_TRAVERSAL = """
MATCH (c:Candidate)
      -[:WORKED_ON]->(p:Project)
      -[:USES_SKILL]->(s:Skill)

RETURN
    c.name AS candidate,
    p.name AS project,
    s.name AS skill

ORDER BY candidate
"""