.PHONY: tests

run:
	@ENV=local python -m b2w.server

migrations:
	@ENV=local python -m b2w.migrations

tests:
	@ENV=tests python -m unittest discover tests -p 'test*'
