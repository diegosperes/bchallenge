.PHONY: tests

run:
	@python -m b2w.server

migrations:
	@python -m b2w.migrations

tests:
	@python -m unittest discover tests -p 'test*'
