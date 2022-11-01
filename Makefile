init:
    pip install -r requirements.txt
	.\scripts\ExportEnvVars.ps1

run:
	python -m flask --app pytrade --debug run

.PHONY: init run