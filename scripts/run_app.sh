#!/bin/bash

port=${PORT:-28900}
FLASK_APP=api.py flask run --port $port