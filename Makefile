.DEFAULT_GOAL := run

.PHONY: run
run: virtualenv_run
	python yelpdor.py

virtualenv_run: requirements.txt requirements-dev.txt
	bin/venv-update venv= -p python2.7 virtualenv_run install= -r requirements-dev.txt
	virtualenv_run/bin/pre-commit autoupdate
	virtualenv_run/bin/pre-commit install

.PHONY: clean
clean:
	find . -iname '*.pyc' -delete
	rm -rf ./virtualenv_run
