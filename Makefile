setup:
	pip install poetry
	poetry env activate
	poetry lock
	poetry install
lint:
	poetry run ruff check src --fix
	poetry run ruff check tests --fix
format:
	poetry run ruff format src
	poetry run ruff format tests
test:
	coverage run -m pytest -v .\tests
	coverage report -m
