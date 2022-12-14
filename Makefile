init:
    pip install -r requirements.txt

lint:
	python -m flake8 --max-line-length 150

test:
	python -m coverage run --source=pytrade -m pytest -v tests

coverage:
    python -m coverage report -m

run:
	python -m flask --debug run

.PHONY: init test run