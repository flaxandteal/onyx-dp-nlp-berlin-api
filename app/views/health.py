from datetime import datetime

from flask import Blueprint

from app.healthcheck import OK, Healthcheck
from app.logger import logger

start_time = datetime.now()

health_check = Healthcheck(status=OK, checks=[], start_time=start_time)

health_blueprint = Blueprint("health", __name__)


@health_blueprint.route("/health", methods=["GET"])
def health():
    return health_check.to_json()
