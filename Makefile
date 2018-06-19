test:
	pipenv run -- python -m unittest discover . "*_test.py"

setup:
	pip install pipenv
	pipenv install --dev --three

.PHONY: test