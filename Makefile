init:
    pip install -r requirements.txt

test:
	python -m pytest

run:
	python -m flask --app pytrade --debug run

.PHONY: init test run