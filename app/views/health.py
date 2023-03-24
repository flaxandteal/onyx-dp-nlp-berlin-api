from flask import Blueprint, Response
from app.logger import configure_logging, setup_logger

configure_logging()
logger = setup_logger(severity=3)

health_blueprint = Blueprint("health", __name__)


@health_blueprint.route("/health", methods=["GET"])
def health():
    return Response('"OK"', status=200)
