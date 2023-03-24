from flask import Blueprint, Response
from logger import configure_logging, setup_logger

configure_logging()
logger = setup_logger()

status_blueprint = Blueprint("status", __name__)


@status_blueprint.route("/status", methods=["GET"])
def status():
    return Response(status=200)
