.PHONY: help install dev format lint type-check test test-cov clean all

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make dev          - Install all dependencies including dev"
	@echo "  make format       - Format code with ruff"
	@echo "  make lint         - Lint code with ruff"
	@echo "  make type-check   - Type check with mypy"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make clean        - Clean up generated files"
	@echo "  make all          - Run format, lint, type-check, and test"

install:
	uv sync --no-dev

dev:
	uv sync --all-extras
	uv pip install -e .

format:
	uv run ruff format src/
	uv run ruff check --fix src/

lint:
	uv run ruff check src/

type-check:
	uv run mypy src/

test:
	uv run pytest

test-cov:
	uv run pytest --cov=src --cov-report=html --cov-report=term

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/

all: format lint type-check test 