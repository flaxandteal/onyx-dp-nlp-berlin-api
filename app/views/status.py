from flask import Blueprint, Response
from logger import logger
status_blueprint = Blueprint("status", __name__)


@status_blueprint.route("/status", methods=["GET"])
def status():
    return Response(status=200)
