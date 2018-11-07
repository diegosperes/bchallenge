.PHONY: tests

run:
	@python -m b2w.server

tests:
	@python -m unittest discover tests -p 'test*'
