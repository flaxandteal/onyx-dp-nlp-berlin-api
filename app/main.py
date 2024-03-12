from flask import Flask

from app.logger import setup_logging
from app.settings import settings
from app.views.berlin import berlin_blueprint
from app.views.health import health_blueprint

logger = setup_logging()


def create_app():
    application = Flask(__name__)
    application.register_blueprint(berlin_blueprint)
    application.register_blueprint(health_blueprint)
    raise Exception("Intentional crash during Gunicorn startup")
    return application


if __name__ == "__main__":
    application = create_app()
    application.run(port=settings.PORT, host="0.0.0.0")
