from flask import Blueprint, jsonify, request

from app.logger import setup_logging
from app.models import LocationModel, MatchModel
from app.store import get_db

logger = setup_logging()
db = get_db()

berlin_blueprint = Blueprint("berlin", __name__)


@berlin_blueprint.route("/berlin/code/<key>", methods=["GET"])
def berlin_code(key):
    try:
        loc = db.retrieve(key)

    except Exception as e:
        logger.error(
            event="error retrieving key from database ",
            error=str(e),
        )

        return jsonify({"key": key, "error": "Not found"}), 404

    location = LocationModel.from_location(loc, db)
    return jsonify(location.to_json()), 200


@berlin_blueprint.route("/berlin/search", methods=["GET"])
def berlin_search():
    q = request.args.get("q")
    state = request.args.get("state") or "gb"
    limit = request.args.get("limit", type=int) or 10
    lev_distance = request.args.get("lev_distance", type=int) or 2

    try:
        logger.info(
            event="Querying database",
            data={
                "q": q,
                "state": state,
                "limit": limit,
                "lev_distance": lev_distance,
            },
        )

        result = db.query(q, state=state, limit=limit, lev_distance=lev_distance)

        matches = [
            {
                "loc": LocationModel.from_location(loc, db).to_json(),
                "scores": MatchModel.from_location(loc).to_json(),
            }
            for loc in result
        ]

        if matches:
            start_idx = matches[0]["scores"]["offset"][0]
            end_idx = matches[0]["scores"]["offset"][1]
            q = q[:start_idx] + q[end_idx:]

        locations = {"query": q, "matches": matches}
        return jsonify(locations), 200

    except Exception as e:
        logger.error(
            event="error querying the database ",
            error=str(e),
        )
        return (
            jsonify({"error": "error querying the database"}),
            500,
        )
