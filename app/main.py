from flask import Flask
import logging
import sys

from app.views.berlin import berlin_blueprint
from app.views.health import health_blueprint
from app.settings import settings, get_custom_settings
from app.logger import configure_logging, setup_logger

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

configure_logging()
logger = setup_logger()

logger.info("initial configuration", data=get_custom_settings())

def create_app():
    application = Flask(__name__)
    application.register_blueprint(berlin_blueprint)
    application.register_blueprint(health_blueprint)
    return application


if __name__ == "__main__":
    application = create_app()
    application.run(
        port=settings.PORT
    )
