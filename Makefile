GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
CYAN   := $(shell tput -Txterm setaf 6)
RESET  := $(shell tput -Txterm sgr0)

EXISTS_POETRY := $(shell command -v poetry 2> /dev/null)
EXISTS_FLASK := $(shell command -v uvicorn 2> /dev/null)

export BERLIN_API_PORT ?= 28900
export BERLIN_API_HOST ?= 0.0.0.0
export FLASK_APP ?= app/main.py

export BERLIN_API_GIT_COMMIT=$(shell git rev-parse HEAD)
export BERLIN_API_VERSION ?= 0.1.0
export BERLIN_API_BUILD_TIME=$(shell date +%s)

.PHONY: all audit build build-bin deps help lint run test-component unit

all: audit lint format

audit: ## audits code for vulnerable dependencies
	poetry run safety check -i 51457 

build:
	docker build --build-arg build_time="${BUILD_TIME}" --build-arg commit="${GIT_COMMIT}" --build-arg version="${VERSION}" -t berlin_api .

build-bin:
	poetry build

deps: ## Installs dependencies
	@if [ -z "$(EXISTS_FLASK)" ]; then \
	if [ -z "$(EXISTS_POETRY)" ]; then \
		pip -qq install poetry; \
		poetry config virtualenvs.in-project true; \
	fi; \
		poetry install --quiet || poetry install; \
	fi; \
	
format: ## Formats your code automatically.
	poetry run isort .
	poetry run black .

lint: ## Lints code 
	poetry run ruff .

run: ## Start the api locally on port 28900.
	FLASK_APP=${FLASK_APP} poetry run flask run --port ${BERLIN_API_PORT}

run-container:
	docker run --env BUILD_TIME='${BUILD_TIME}' -e GIT_COMMIT="${GIT_COMMIT}" -e VERSION="${VERSION}" -ti berlin_api


test-component: ## runs component tests
	poetry run pytest -v tests/api


unit: ## runs component tests
	poetry run pytest -v tests/unit

help: ## Show this help.
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} { \
		if (/^[a-zA-Z_-]+:.*?##.*$$/) {printf "    ${YELLOW}%-20s${GREEN}%s${RESET}\n", $$1, $$2} \
		else if (/^## .*$$/) {printf "  ${CYAN}%s${RESET}\n", substr($$1,4)} \
		}' $(MAKEFILE_LIST)

