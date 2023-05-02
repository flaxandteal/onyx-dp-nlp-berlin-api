from flask import Blueprint, Response
from app.logger import configure_logging, setup_logger
from app.healthcheck import *

configure_logging()
logger = setup_logger(severity=3)

health_check = Healthcheck(status=OK, version='0.1.0', checks=[])

health_blueprint = Blueprint("health", __name__)


@health_blueprint.route("/health", methods=["GET"])
def health():
    return health_check.to_json()
