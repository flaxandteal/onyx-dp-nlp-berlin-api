from flask import Blueprint, jsonify, request

from app.logger import configure_logging, setup_logger
from app.models import LocationModel
from app.store import get_db

configure_logging()
logger = setup_logger()

db = get_db()

berlin_blueprint = Blueprint("berlin", __name__)


@berlin_blueprint.route("/berlin/code/<key>", methods=["GET"])
def berlin_code(key):
    try:
        loc = db.retrieve(key)

    except Exception as e:
        logger.error(
            event="error retrieving key from database ",
            stack_trace=str(e),
            level="ERROR",
            severity=1,
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
        log_message = f"Querying database with q={q}, state={state}, limit={limit}, lev_distance={lev_distance}"
        logger.info(log_message, severity=0)

        result = db.query(q, state=state, limit=limit, lev_distance=lev_distance)

        locations = {
            "matches": [
                LocationModel.from_location(loc, db).to_json() for loc in result
            ]
        }
        return jsonify(locations), 200

    except Exception as e:
        logger.error(
            event="error querying the database ",
            stack_trace=str(e),
            level="ERROR",
            severity=1,
        )
        return (jsonify({"error": "error querying the database"}), 500,)
