from flask import Flask

from app.views.berlin import berlin_blueprint
from app.views.health import health_blueprint
from app.settings import HOST, PORT


def create_app():
    application = Flask(__name__)
    application.register_blueprint(berlin_blueprint)
    application.register_blueprint(health_blueprint)
    return application


if __name__ == "__main__":
    application = create_app()
    application.run(
        port=PORT,
        host=HOST
    )
