@default:
  @just --list

@build: test lint check
  echo 'Run flit build'
  pipenv run flit build

@check:
  echo 'Run ruff format --check'
  pipenv run ruff format --check

@clean:
  rm dist/*
  rmdir dist

@format:
  echo 'Run ruff format'
  pipenv run ruff format

@lint:
  echo 'Run ruff check'
  pipenv run ruff check

@test:
  echo 'Run pytest'
  pipenv run pytest

@publish: build
  echo 'Run flit publish'
  pipenv run flit publish
