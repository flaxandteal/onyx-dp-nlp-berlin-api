from flask import Blueprint, jsonify, request
from requests import RequestException

from app.logger import configure_logging, setup_logger
from app.store import get_db
from app.models import LocationModel

configure_logging()
logger = setup_logger()

db = get_db()

berlin_blueprint = Blueprint("berlin", __name__)


@berlin_blueprint.route("/berlin/code/<key>", methods=["GET"])
def berlin_code(key):
    try:
        loc = db.retrieve(key)
    except KeyError:
        return jsonify({
            "key": key,
            "error": "Not found"
        }), 404

    location = LocationModel.from_location(loc, db)
    return jsonify(location.to_json()), 200


@berlin_blueprint.route("/berlin/search", methods=["GET"])
def berlin_search():
    q = request.args.get("q")
    state = request.args.get("state")
    limit = request.args.get("limit", type=int)
    lev_distance = request.args.get("lev_distance", type=int)

    try:
        result = db.query(
            q, state=state, limit=limit or 10, lev_distance=lev_distance or 2
        )
        locations = {
            "matches": [
                LocationModel.from_location(loc, db).to_json()
                for loc in result
            ]
        }
        return jsonify(locations), 200

    except RequestException:
        logger.error("there was an error querying the database")
        return jsonify(error="there was an error querying the database"), 500
