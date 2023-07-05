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

RUN poetry install --no-dev

EXPOSE 28900

ENV FLASK_APP=app/main.py

ENTRYPOINT flask run --host 0.0.0.0 --port 28900

