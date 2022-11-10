init:
    pip install -r requirements.txt

test:
	python -m pytest

run:
	python -m flask --debug run

.PHONY: init test run