GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
CYAN   := $(shell tput -Txterm setaf 6)
RESET  := $(shell tput -Txterm sgr0)

.PHONY: build run lint test help

build: ## Builds a binary file 
	poetry run ./scripts/build.sh

lint: ## Lints code 
	poetry run ./scripts/run_lint_python.sh

test: ## Runs all available tests and generates a coverage report located in htmlcov
	poetry run ./scripts/run_tests_unit.sh

format: ## Formats your code automatically.
	poetry run isort .
	poetry run black .


run: ## Start the api locally on port 3001. endpoints: /health, /berlin/search?q=query
	poetry run ./scripts/run_app.sh

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

