GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
CYAN   := $(shell tput -Txterm setaf 6)
RESET  := $(shell tput -Txterm sgr0)

EXISTS_POETRY := $(shell command -v poetry 2> /dev/null)
EXISTS_FLASK := $(shell command -v uvicorn 2> /dev/null)

.PHONY: build run lint test help audit deps

audit: deps ## Makes sure dep are installed and audits code for vulnerable dependencies
	pip install safety
	safety check

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
	poetry run ./scripts/run_lint_python.sh

run: deps ## Start the api locally on port 3001. endpoints: /health, /berlin/search?q=query
	poetry run ./scripts/run_app.sh

test: deps ## Runs all available tests and generates a coverage report located in htmlcov
	poetry run ./scripts/run_tests_unit.sh

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

