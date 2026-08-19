import os

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
    CAREER_PATH,
)


app = Flask(__name__)

# Create database connection
db = Database()


# ============================================================
# HOME / DASHBOARD
# ============================================================

@app.route("/")
def index():
    try:
        candidates = db.query(GET_CANDIDATES)

        return render_template(
            "index.html",
            candidates=candidates,
            error=None
        )

    except Exception as error:
        print("HOME ERROR:", error)

        return render_template(
            "index.html",
            candidates=[],
            error="Unable to connect to the graph database."
        )


# ============================================================
# ALL CANDIDATES
# ============================================================

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
            search=search,
            error=None
        )

    except Exception as error:
        print("CANDIDATES ERROR:", error)

        return render_template(
            "candidates.html",
            candidates=[],
            search=search,
            error="Unable to load candidates."
        )


# ============================================================
# CANDIDATE DETAILS
# ============================================================

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
            ), 404

        return render_template(
            "candidate_detail.html",
            candidate=result[0],
            error=None
        )

    except Exception as error:
        print("CANDIDATE ERROR:", error)

        return render_template(
            "candidate_detail.html",
            candidate=None,
            error="Unable to load candidate."
        ), 503


# ============================================================
# CANDIDATES BY SKILL API
# ============================================================

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

    except Exception as error:
        print("SKILL ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to load candidates for this skill."
        }), 503


# ============================================================
# CANDIDATES FOR ROLE API
# ============================================================

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

    except Exception as error:
        print("ROLE CANDIDATES ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to load candidates for this role."
        }), 503


# ============================================================
# SIMILAR CANDIDATES PAGE
# ============================================================

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
            candidate_id=candidate_id,
            error=None
        )

    except Exception as error:
        print("SIMILAR CANDIDATES ERROR:", error)

        return render_template(
            "similar_candidates.html",
            results=[],
            candidate_id=candidate_id,
            error="Unable to find similar candidates."
        ), 503


# ============================================================
# SIMILAR CANDIDATES API
# ============================================================

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

    except Exception as error:
        print("SIMILAR CANDIDATES API ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to find similar candidates."
        }), 503


# ============================================================
# GRAPH EXPLORER
# ============================================================

@app.route("/graph")
def graph():
    try:
        results = db.query(MULTI_HOP_TRAVERSAL)

        return render_template(
            "graph.html",
            results=results,
            error=None
        )

    except Exception as error:
        print("GRAPH ERROR:", error)

        return render_template(
            "graph.html",
            results=[],
            error="Unable to load graph relationships."
        ), 503


# ============================================================
# CAREER EXPLORER PAGE
# ============================================================

@app.route("/careers")
def careers():
    return render_template(
        "careers.html",
        error=None
    )


# ============================================================
# CAREER PATH API
# ============================================================

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

    except Exception as error:
        print("CAREER PATH API ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to load career paths."
        }), 503


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():
    try:
        db.verify()

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except Exception as error:
        print("HEALTH ERROR:", error)

        return jsonify({
            "status": "unhealthy",
            "database": "unavailable"
        }), 503


# ============================================================
# 404 HANDLER
# ============================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "index.html",
        candidates=[],
        error="The requested page was not found."
    ), 404


# ============================================================
# 500 HANDLER
# ============================================================

@app.errorhandler(500)
def internal_server_error(error):
    print("INTERNAL SERVER ERROR:", error)

    return render_template(
        "index.html",
        candidates=[],
        error="Something went wrong. Please try again."
    ), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )