from flask import Flask

from app.views.status import status_blueprint
from app.views.berlin import berlin_blueprint

application = Flask(__name__)
application.register_blueprint(berlin_blueprint)
application.register_blueprint(status_blueprint)

if __name__ == "__main__":
    application.run(port=5001)
