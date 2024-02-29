#!/bin/bash -eux

cwd=$(pwd)

pushd dp-nlp-berlin-api
  make build-bin
  mv dist/ $cwd/build
  mv data/ $cwd/build
  cp Dockerfile.concourse $cwd/build
  cp gunicorn_config.py $cwd/build
  cp .env.default $cwd/build
popd
