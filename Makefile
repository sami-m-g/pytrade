init:
    pip install -r requirements.txt
	.\scripts\ExportEnvVars.ps1

test:
	python -m pytest

run:
	python -m flask --app pytrade --debug run

.PHONY: init test run