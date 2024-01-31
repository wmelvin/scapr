@default:
  @just --list

# Run test, lint, check, flit build
@build: test lint check
  pipenv run flit build

# Check formatting with ruff
@check:
  pipenv run ruff format --check

# Run test, lint, check, then pipenv check
@checks: test lint check
  pipenv check

# Clean up dist folder
@clean:
  rm dist/*

# Apply ruff formatting
@format:
  pipenv run ruff format

# Chcek linting with ruff
@lint:
  pipenv run ruff check

# Run pytest
@test:
  pipenv run pytest

# Build and publish using flit
@publish: build
  pipenv run flit publish
