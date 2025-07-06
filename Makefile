.PHONY: help setup install test lint format clean run docker-build docker-run migrate

# Default target
help:
	@echo "Available commands:"
	@echo "  setup         - Set up development environment"
	@echo "  install       - Install dependencies"
	@echo "  test          - Run tests"
	@echo "  lint          - Run linters"
	@echo "  format        - Format code"
	@echo "  clean         - Clean temporary files"
	@echo "  run           - Run the bot"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run with Docker Compose"
	@echo "  migrate       - Run database migrations"

# Setup development environment
setup:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install -r requirements-dev.txt
	./venv/bin/pre-commit install
	@echo "Setup complete! Don't forget to configure your .env file"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Run tests
test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

# Run linters
lint:
	flake8 src/ tests/
	mypy src/
	bandit -r src/

# Format code
format:
	black src/ tests/
	isort src/ tests/

# Clean temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

# Run the bot
run:
	python -m src.bot.main

# Build Docker image
docker-build:
	docker build -t telegram-bot .

# Run with Docker Compose
docker-run:
	docker-compose up -d

# Stop Docker containers
docker-stop:
	docker-compose down

# Run database migrations
migrate:
	alembic upgrade head

# Create new migration
migration:
	alembic revision --autogenerate -m "$(MSG)"

# Run pre-commit hooks
pre-commit:
	pre-commit run --all-files

# Development server with auto-reload
dev:
	python -m src.bot.main --reload

# Check code quality
check: lint test

# Full CI pipeline
ci: clean format lint test

# Production deployment
deploy:
	docker-compose -f docker-compose.yml up -d --build

# View logs
logs:
	docker-compose logs -f bot

# Database shell
db-shell:
	docker-compose exec postgres psql -U bot_user -d telegram_bot

# Redis shell
redis-shell:
	docker-compose exec redis redis-cli