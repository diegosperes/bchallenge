.PHONY: tests

run:
	@python server.py

tests:
	@python -m unittest discover tests -p 'test*'
