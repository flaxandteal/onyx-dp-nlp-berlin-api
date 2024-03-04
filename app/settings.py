import time

from dynaconf import Dynaconf

current_time = int(time.time())

settings = Dynaconf(
    envvar_prefix="BERLIN_API",
    load_dotenv=True,
    dotenv_path=".env.default",
)

settings.reload()

settings.HOST = settings.get("HOST", "0.0.0.0")
settings.PORT = settings.get("PORT", "28900")
settings.NAMESPACE = settings.get("LOGGING_NAMESPACE", "dp-nlp-berlin-api")
settings.DATA_LOCATION = settings.get("DATA_LOCATION", "/data")
settings.BUILD_TIME = settings.get("BUILD_TIME", current_time)
settings.GIT_COMMIT = settings.get("GIT_COMMIT")


def get_custom_settings():
    custom_settings = {}
    vars = ["HOST", "PORT", "NAMESPACE", "DATA_LOCATION", "BUILD_TIME", "GIT_COMMIT"]
    for v in vars:
        custom_settings[v] = settings[v]

    return custom_settings
