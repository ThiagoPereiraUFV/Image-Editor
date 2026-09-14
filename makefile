.PHONY: run lint format test coverage clean

run:
	uv run image-editor

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

test:
	uv run pytest

coverage:
	uv run pytest --cov-report=html

clean:
	rm -rf .venv .pytest_cache .coverage htmlcov
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
