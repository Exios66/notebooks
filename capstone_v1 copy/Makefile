.PHONY: help install test lint format type-check clean build

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code with black"
	@echo "  make type-check   - Run type checking"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make build        - Build package"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=api_wrapper --cov-report=term-missing

lint:
	flake8 api_wrapper/ tests/ --max-line-length=100
	black --check api_wrapper/ tests/
	mypy api_wrapper/ --ignore-missing-imports || true

format:
	black api_wrapper/ tests/

type-check:
	mypy api_wrapper/ --ignore-missing-imports

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

build:
	python -m build

