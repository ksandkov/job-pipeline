# job-pipeline — dev tasks
.PHONY: dev lint test build run migrate

dev:      ## Install with dev extras
	pip install -e ".[dev]"

lint:     ## Ruff lint + format check
	ruff check .
	ruff format --check .

test:     ## Run tests with coverage
	pytest

build:    ## Build the Docker image
	docker build -t job-pipeline:local .

run:      ## Run the API locally
	uvicorn jobpipeline.main:app --reload --port 8000

migrate:  ## Apply DB migrations
	alembic upgrade head
