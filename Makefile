.PHONY: help install install-dev test lint format clean run example

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make run          - Run the MCP server"
	@echo "  make example      - Run example client"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest -v

test-coverage:
	pytest --cov=src --cov-report=html --cov-report=term

lint:
	ruff check src/ tests/ examples/
	mypy src/

format:
	black src/ tests/ examples/ scripts/
	ruff check --fix src/ tests/ examples/

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

run:
	python -m src.server

example:
	python examples/example_client.py

