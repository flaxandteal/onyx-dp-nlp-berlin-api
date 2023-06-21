import time
from dynaconf import Dynaconf

current_time = int(time.time())

settings = Dynaconf(
    envvar_prefix="BERLIN_API",
    load_dotenv=True,
    dotenv_path=".env.default",
)

settings.reload()

settings.HOST = settings.get("HOST")
settings.PORT = settings.get("PORT")
settings.NAMESPACE = settings.get("LOGGING_NAMESPACE")
settings.DATA_LOCATION = settings.get("DATA_LOCATION")
settings.BUILD_TIME = settings.get("BUILD_TIME", current_time)
settings.GIT_COMMIT = settings.get("GIT_COMMIT")