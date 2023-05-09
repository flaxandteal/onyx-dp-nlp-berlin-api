from flask import Blueprint

from app.healthcheck import Healthcheck, OK
from app.logger import configure_logging, setup_logger

configure_logging()
logger = setup_logger(severity=3)

health_check = Healthcheck(status=OK, version="0.1.0", checks=[])

health_blueprint = Blueprint("health", __name__)


@health_blueprint.route("/health", methods=["GET"])
def health():
    return health_check.to_json()
