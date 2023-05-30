GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
CYAN   := $(shell tput -Txterm setaf 6)
RESET  := $(shell tput -Txterm sgr0)

EXISTS_POETRY := $(shell command -v poetry 2> /dev/null)
EXISTS_FLASK := $(shell command -v uvicorn 2> /dev/null)

BERLIN_API_PORT ?= 28900
FLASK_APP ?= api.py

export START_TIME=$(shell date +%s)
export GIT_COMMIT=$(shell git rev-parse HEAD)
export VERSION ?= 0.1.0

.PHONY: build run lint test help audit deps all

all: audit lint format

audit: deps ## Makes sure dep are installed and audits code for vulnerable dependencies
	poetry run safety check -i 51457 

build: deps
	docker build -t berlin_api .
build-bin: deps ## Builds a binary file 
	poetry run ./scripts/build.sh

deps: ## Installs dependencies
	@if [ -z "$(EXISTS_FLASK)" ]; then \
	if [ -z "$(EXISTS_POETRY)" ]; then \
		pip -qq install poetry; \
		poetry config virtualenvs.in-project true; \
	fi; \
		poetry install --quiet || poetry install; \
	fi; \

lint: deps ## Lints code 
	poetry run ruff .

run: deps ## Start the api locally on port 28900.
	FLASK_APP=${FLASK_APP} poetry run flask run --port ${BERLIN_API_PORT}

test: deps ## Runs all available tests and generates a coverage report located in htmlcov
	poetry run ./scripts/run_tests_unit.sh

.PHONY: test-component
test-component: deps ## Makes sure dep are installed and runs component tests
	poetry run pytest tests/api

format: deps ## Formats your code automatically.
	poetry run isort .
	poetry run black .

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

