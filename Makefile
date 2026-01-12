.PHONY: help install test lint format type-check clean docker-build docker-run demo pre-commit

# Default target
help:
	@echo "eBay Listing Automation - Available Commands"
	@echo "============================================="
	@echo "make install      - Install dependencies"
	@echo "make test         - Run tests with coverage"
	@echo "make lint         - Run linters (ruff, flake8)"
	@echo "make format       - Format code with black and isort"
	@echo "make type-check   - Run mypy type checking"
	@echo "make pre-commit   - Run all pre-commit hooks"
	@echo "make clean        - Remove build artifacts"
	@echo "make docker-build - Build Docker image"
	@echo "make docker-run   - Run Docker container"
	@echo "make demo         - Run the demo"

# Install dependencies
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install pytest pytest-cov black isort ruff mypy pre-commit

# Run tests with coverage
test:
	pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html

# Run linters
lint:
	ruff check .
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Format code
format:
	black .
	isort .
	ruff check --fix .

# Type checking
type-check:
	mypy . --ignore-missing-imports

# Run pre-commit hooks
pre-commit:
	pre-commit run --all-files

# Clean build artifacts
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Docker commands
docker-build:
	docker build -t ebay-listing-automation .

docker-run:
	docker run --rm -it ebay-listing-automation

# Run demo
demo:
	python demo.py
