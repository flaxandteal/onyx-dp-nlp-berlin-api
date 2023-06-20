import time
from dynaconf import Dynaconf

current_time = int(time.time())

settings = Dynaconf(
    envvar_prefix="BERLIN_API",
    load_dotenv=True,
    dotenv_path=".env.default",
)

settings.reload()

HOST = settings.get("HOST")
PORT = settings.get("PORT")

NAMESPACE = settings.get("LOGGING_NAMESPACE")
DATA_LOCATION = settings.get("DATA_LOCATION")

# BERLIN_API_START_TIME name of the start_time variable
BUILD_TIME = settings.get("BUILD_TIME", current_time)
GIT_COMMIT = settings.get("GIT_COMMIT")
