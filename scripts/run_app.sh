#!/bin/bash

port=${PORT:-3001}
FLASK_APP=api.py flask run --port $port