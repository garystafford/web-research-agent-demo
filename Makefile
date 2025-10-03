.PHONY: format lint test clean install dev-install

# Variables
# PYTHON = python3
# PIP = $(PYTHON) -m pip
UV = uv
UVX = uvx

# Default target
all: format lint test

# Activate virtual environment
source:
	@if [ ! -d ".venv" ]; then \
		$(UV) venv; \
	fi
	@

# Format code with Black and isort
format:
	$(UVX) autoflake --remove-all-unused-imports --in-place *.py
	$(UVX) isort *.py
	$(UVX) black *.py

# Run linting checks
lint:
	$(UVX) flake8 *.py
	$(UVX) mypy --ignore-missing-imports *.py

# Run tests
test:
	$(UVX) pytest

# Install dependencies
install:
	$(UV) sync

# Upgrade dependencies
upgrade:
	$(UV) lock --upgrade

# Clean up temporary files
clean:
	rm -rf __pycache__/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run the application
run:
	$(UV) run agent.py