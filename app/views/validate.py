import json
from json import JSONDecodeError

from flask import Blueprint, Response, jsonify, request
from requests import RequestException
from structlog import get_logger

logger = get_logger()

berlin_blueprint = Blueprint("berlin", __name__)


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
    try:
        json_search_parameters = json.loads(request.data.decode())
    except JSONDecodeError:
        logger.info("Could not parse JSON", status=400)
        return Response(status=400, response="Could not parse JSON")

    response = {}
    try:
        # get response
        locations = True

    except RequestException:
        logger.info("Berlin error [TODO: more information]")
        return jsonify(error="Berlin error [TODO: more information]")

    if len(locations) == 0:
        logger.info("No locations found", status=404)
        return jsonify(response), 404

    logger.info("Found location", status=200)

    return jsonify(response), 200
