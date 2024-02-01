FROM python:3.10-slim

RUN apt-get update && apt-get install --no-install-recommends -y git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN mkdir -p /usr/src/
WORKDIR /usr/src/

COPY app /usr/src/app
COPY data /usr/src/data
COPY .env.default poetry.lock pyproject.toml /usr/src/
COPY gunicorn_config.py /usr/src/

RUN poetry install --no-dev

EXPOSE 28900

ENV FLASK_APP=app/main.py

ENTRYPOINT poetry run gunicorn "app.main:create_app()" -b 0.0.0.0:28900 -c gunicorn_config.py

