.DEFAULT_GOAL := virtualenv_run

virtualenv_run: requirements.txt requirements-dev.txt
	bin/venv-update venv= -p python2.7 virtualenv_run install= -r requirements-dev.txt

.PHONY: clean
clean:
	find . -iname '*.pyc' -delete
	rm -rf ./virtualenv_run
