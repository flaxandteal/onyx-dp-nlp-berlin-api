import json
from datetime import datetime
import berlin
import time


from json import JSONDecodeError
from app.views.healthcheck import Healthcheck
from flask import Blueprint, Response, jsonify, request
from requests import RequestException
from structlog import get_logger

start_time = datetime.utcnow().isoformat()
uptime = time.time()

health = Healthcheck(status="OK", version='1.0.0', uptime=uptime, start_time=start_time, checks=[])

logger = get_logger()

berlin_blueprint = Blueprint("berlin", __name__)
   
db = berlin.load("data")

@berlin_blueprint.route("/health", methods=["GET"])
def healthcheck():
    logger.info("Fetch healthcheck")
    return health.to_json(), 200

@berlin_blueprint.route("/berlin/fetch-schema", methods=["GET"])
def berlin_fetch_schema():
    logger.info("Fetch schema")
    return jsonify({}), 200


@berlin_blueprint.route("/berlin/code/:key", methods=["GET"])
def berlin_code():
    logger.info("Retrieve code")
    return jsonify({}), 200


@berlin_blueprint.route("/berlin/search-schema", methods=["GET"])
def berlin_search_schema():
    logger.info("Search schema")
    return jsonify({}), 200


@berlin_blueprint.route("/berlin/search", methods=["GET"])
def berlin_search():
    json_search_parameters = request.args
    #try:
    #    json_search_parameters = json.loads(request.data.decode())
    #except JSONDecodeError:
    #    logger.info("Could not parse JSON", status=400)
    #    return Response(status=400, response="Could not parse JSON")

    # validate
    query = json_search_parameters["q"]
    # state = json_search_parameters["state"]
    # limit = json_search_parameters.get("limit", 1)
    # lev_distance = max(int(json_search_parameters.get("ld", 2)), 2)


    try:
        result = db.query(query, "berlin", 1, 2)
        locations = {
            "matches": [
                {
                    "key": loc.key,
                    "encoding": loc.encoding,
                    "id": loc.id,
                    "words": loc.words
                }
                for loc in result
            ]
        }

    except RequestException:
        logger.info("Berlin error [TODO: more information]")
        return jsonify(error="Berlin error [TODO: more information]")

    return jsonify(locations), 200
