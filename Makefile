precommit-check:
	@echo "Running ruff, linting, pytest, and coverage check..."
	@ruff check --fix --ignore F401,E501,F811
	@ruff check --ignore F401,E501,F811
	@pytest --maxfail=1 --disable-warnings -q
	@coverage run -m pytest
	@coverage report -m
	@coverage html
	@echo "Ruff, linting, pytest, and coverage check completed."

start-local:
	@echo "Starting local server..."
	export PYTHONPATH=$(shell pwd) && python app/main.py
	@echo "Local server started."