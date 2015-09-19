BIN := virtualenv_run/bin
PYTHON := $(BIN)/python
SHELL := /bin/bash
RANDOM_PORT := $(shell expr $$(( 8000 + (`id -u` % 1000) )))

.PHONY: check dev venv clean lint test gunicorn

check: lint test

lint: venv
	$(BIN)/pre-commit run --all-files

test: venv
	$(BIN)/py.test tests/

dev: venv scss
	@echo "Running on port $(RANDOM_PORT)"
	$(PYTHON) ./manage.py runserver 0.0.0.0:$(RANDOM_PORT)

venv:
	python ./bin/venv-update -ppython3 virtualenv_run requirements.txt requirements-dev.txt

clean:
	rm -rf *.egg-info
	rm -rf virtualenv_run

# closer to prod
gunicorn: venv
	@echo "Running on port $(RANDOM_PORT)"
	$(BIN)/gunicorn -b 0.0.0.0:$(RANDOM_PORT) ocfweb.wsgi

scss: venv
	$(PYTHON) setup.py build_sass

watch-scss: scss
	while :; do \
		find ocfweb/static -type f -name '*.scss' | \
			inotifywait --fromfile - -e modify; \
			make scss; \
	done

update-requirements:
	$(eval TMP := $(shell mktemp -d))
	virtualenv -p python3 $(TMP)
	. $(TMP)/bin/activate && \
		pip install --upgrade pip && \
		pip install . && \
		pip freeze | grep -v '^ocfweb==' | sed 's/^ocflib==.*/ocflib/' > requirements.txt
