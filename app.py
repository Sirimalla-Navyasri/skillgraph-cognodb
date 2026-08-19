from flask import Flask, render_template, request, jsonify

from database.connection import Database
from database.queries import (
    GET_CANDIDATES,
    GET_CANDIDATE,
    MULTI_HOP_TRAVERSAL,
    SEARCH_CANDIDATES,
    CANDIDATES_BY_SKILL,
    CANDIDATES_FOR_ROLE,
    SIMILAR_CANDIDATES,
    CAREER_PATH
)

app = Flask(__name__)

db = Database()


# ==================================================
# HOME / DASHBOARD
# ==================================================

@app.route("/")
def index():
    try:
        candidates = db.query(GET_CANDIDATES)

        return render_template(
            "index.html",
            candidates=candidates
        )

    except Exception as e:
        print("HOME ERROR:", e)

        return render_template(
            "index.html",
            candidates=[],
            error="Unable to connect to the graph database."
        )


# ==================================================
# ALL CANDIDATES
# ==================================================

@app.route("/candidates")
def candidates():
    search = request.args.get("search", "").strip()

    try:
        if search:
            results = db.query(
                SEARCH_CANDIDATES,
                {
                    "search": search
                }
            )
        else:
            results = db.query(GET_CANDIDATES)

        return render_template(
            "candidates.html",
            candidates=results,
            search=search
        )

    except Exception as e:
        print("CANDIDATES ERROR:", e)

        return render_template(
            "candidates.html",
            candidates=[],
            search=search,
            error="Unable to load candidates."
        )


# ==================================================
# CANDIDATE DETAILS
# ==================================================

@app.route("/candidate/<candidate_id>")
def candidate(candidate_id):
    try:
        result = db.query(
            GET_CANDIDATE,
            {
                "candidate_id": candidate_id
            }
        )

        if not result:
            return render_template(
                "candidate_detail.html",
                candidate=None,
                error="Candidate not found."
            )

        return render_template(
            "candidate_detail.html",
            candidate=result[0]
        )

    except Exception as e:
        print("CANDIDATE ERROR:", e)

        return render_template(
            "candidate_detail.html",
            candidate=None,
            error="Unable to load candidate."
        )


# ==================================================
# CANDIDATES BY SKILL API
# ==================================================

@app.route("/api/skill/<skill>")
def skill_candidates(skill):
    try:
        results = db.query(
            CANDIDATES_BY_SKILL,
            {
                "skill": skill
            }
        )

        return jsonify({
            "success": True,
            "results": results
        })

    except Exception as e:
        print("SKILL ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 503


# ==================================================
# CANDIDATES FOR ROLE API
# ==================================================

@app.route("/api/role/<role_id>/candidates")
def role_candidates(role_id):
    try:
        results = db.query(
            CANDIDATES_FOR_ROLE,
            {
                "role_id": role_id
            }
        )

        return jsonify({
            "success": True,
            "results": results
        })

    except Exception as e:
        print("ROLE CANDIDATES ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 503


# ==================================================
# SIMILAR CANDIDATES PAGE
# ==================================================

@app.route("/candidate/<candidate_id>/similar")
def similar_candidates_page(candidate_id):
    try:
        results = db.query(
            SIMILAR_CANDIDATES,
            {
                "candidate_id": candidate_id
            }
        )

        return render_template(
            "similar_candidates.html",
            results=results,
            candidate_id=candidate_id
        )

    except Exception as e:
        print("SIMILAR CANDIDATES ERROR:", e)

        return render_template(
            "similar_candidates.html",
            results=[],
            candidate_id=candidate_id,
            error=str(e)
        )


# ==================================================
# SIMILAR CANDIDATES API
# ==================================================

@app.route("/api/candidate/<candidate_id>/similar")
def similar_candidates_api(candidate_id):
    try:
        results = db.query(
            SIMILAR_CANDIDATES,
            {
                "candidate_id": candidate_id
            }
        )

        return jsonify({
            "success": True,
            "results": results
        })

    except Exception as e:
        print("SIMILAR CANDIDATES API ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 503


# ==================================================
# CAREER PATH API
# ==================================================

@app.route("/api/role/<role_id>/career-path")
def api_career_path(role_id):
    try:
        results = db.query(
            CAREER_PATH,
            {
                "role_id": role_id
            }
        )

        return jsonify({
            "success": True,
            "results": results
        })

    except Exception as e:
        print("CAREER PATH API ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 503


# ==================================================
# GRAPH EXPLORER
# ==================================================

@app.route("/graph")
def graph():
    try:
        results = db.query(MULTI_HOP_TRAVERSAL)

        return render_template(
            "graph.html",
            results=results
        )

    except Exception as e:
        print("GRAPH ERROR:", e)

        return render_template(
            "graph.html",
            results=[],
            error="Unable to connect to the graph database."
        )


# ==================================================
# CAREER EXPLORER
# ==================================================

@app.route("/role/<role_id>/career")
def career_path(role_id):
    try:
        results = db.query(
            CAREER_PATH,
            {
                "role_id": role_id
            }
        )

        return render_template(
            "career.html",
            results=results
        )

    except Exception as e:
        print("CAREER PAGE ERROR:", e)

        return render_template(
            "career.html",
            results=[],
            error="Unable to connect to the graph database."
        )


# ==================================================
# HEALTH CHECK
# ==================================================

@app.route("/health")
def health():

    try:
        db.verify()

        return jsonify({
            "status": "healthy",
            "database": "connected"
        })

    except Exception as e:

        print("HEALTH ERROR:", e)

        return jsonify({
            "status": "unhealthy",
            "database": "unavailable",
            "error": str(e)
        }), 503


# ==================================================
# START APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )