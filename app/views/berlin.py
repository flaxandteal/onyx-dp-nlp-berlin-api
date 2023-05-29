from flask import Blueprint, jsonify, request
from requests import RequestException

from app.logger import configure_logging, setup_logger
from app.store import get_db

configure_logging()
logger = setup_logger(severity=3)

db = get_db()

berlin_blueprint = Blueprint("berlin", __name__)


@berlin_blueprint.route("/v1/berlin/fetch-schema", methods=["GET"])
def berlin_fetch_schema():
    logger.info("Fetch schema")
    return jsonify({}), 200


10


@berlin_blueprint.route("/v1/berlin/code/:key", methods=["GET"])
def berlin_code():
    logger.info("Retrieve code")
    return jsonify({}), 200


@berlin_blueprint.route("/v1/berlin/search-schema", methods=["GET"])
def berlin_search_schema():
    logger.info("Search schema")
    return jsonify({}), 200


@berlin_blueprint.route("/v1/berlin/search", methods=["GET"])
def berlin_search():
    q = request.args.get("q")
    state = request.args.get("state")
    limit = request.args.get("limit", type=int)
    lev_distance = request.args.get("lev_distance", 2, type=int)

    try:
        result = db.query(q, state=state, limit=limit or 10, lev_distance=lev_distance or 2)
        locations = {
            "matches": [
                {
                    "key": loc.key,
                    "encoding": loc.encoding,
                    "id": loc.id,
                    "words": loc.words,
                }
                for loc in result
            ]
        }
        return jsonify(locations), 200

    except RequestException:
        logger.info("Berlin error [TODO: more information]")
        return jsonify(error="Berlin error [TODO: more information]"), 500
