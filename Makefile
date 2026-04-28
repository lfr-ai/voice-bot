PYTHON=python

.PHONY: install run test lint format

install:
	pip install -r requirements.txt

run:
	uvicorn voice.interaction.main:app --reload

test:
	pytest -q

lint:
	flake8 src tests

format:
	black .
