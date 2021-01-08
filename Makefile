test:
	poetry run pytest tests

test-cov:
	poetry run pytest tests --cov=dispike

tests-cov-browser:
	poetry run pytest tests --cov=dispike --cov-report=html
	sensible-browser htmlcov/index.html