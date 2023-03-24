import json
from json import JSONDecodeError

from flask import Blueprint, Response, jsonify, request
from requests import RequestException
from logger import configure_logging, setup_logger
import berlin

configure_logging()
logger = setup_logger()

berlin_blueprint = Blueprint("berlin", __name__)

# FIXME: better initting
db = berlin.load("data")


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
    state = json_search_parameters["state"]
    limit = json_search_parameters.get("limit", 1)
    lev_distance = max(int(json_search_parameters.get("ld", 2)), 2)


    try:
        result = db.query(query, state, limit, lev_distance)
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
