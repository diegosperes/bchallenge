.PHONY: tests

setup:
	@pip install -r requirements.txt

migrations:
	@ENV=local python -m b2w.migrations

run:
	@ENV=local python -m b2w.server

tests:
	@ENV=tests python -m unittest discover tests -p 'test*'

build:
	@docker build . -t b2w

run-prod:
	@docker-compose up
