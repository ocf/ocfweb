BIN := virtualenv_run/bin
PYTHON := $(BIN)/python
SHELL := /bin/bash
RANDOM_PORT := $(shell expr $$(( 8000 + (`id -u` % 1000) )))

.PHONY: dev clean lint test coveralls gunicorn

test: virtualenv_run/
	$(BIN)/coverage erase
	$(BIN)/python install_coverage_path.py
	COVERAGE_PROCESS_START=$(PWD)/.coveragerc \
		$(BIN)/py.test -v tests/
	$(BIN)/coverage combine
	$(BIN)/coverage report
	$(BIN)/pre-commit run --all-files

# first set COVERALLS_REPO_TOKEN=<repo token> environment variable
coveralls: virtualenv_run/ test
	$(BIN)/coveralls

dev: virtualenv_run/ scss
	@echo -e "\e[1m\e[93mRunning on http://$(shell hostname -f ):$(RANDOM_PORT)/\e[0m"
	$(PYTHON) ./manage.py runserver 0.0.0.0:$(RANDOM_PORT)

virtualenv_run/: requirements.txt requirements-dev.txt
	python ./bin/venv-update -ppython3 virtualenv_run requirements.txt requirements-dev.txt

clean:
	rm -rf *.egg-info
	rm -rf virtualenv_run

# closer to prod
gunicorn: virtualenv_run/
	@echo "Running on port $(RANDOM_PORT)"
	$(BIN)/gunicorn -b 0.0.0.0:$(RANDOM_PORT) ocfweb.wsgi

scss: virtualenv_run/
	$(PYTHON) setup.py build_sass

watch-scss: scss virtualenv_run
	while :; do \
		find ocfweb/static -type f -name '*.scss' | \
			inotifywait --fromfile - -e modify; \
			$(PYTHON) setup.py build_sass; \
	done

update-requirements:
	$(eval TMP := $(shell mktemp -d))
	virtualenv -p python3 $(TMP)
	. $(TMP)/bin/activate && \
		pip install --upgrade pip && \
		pip install . && \
		pip freeze | grep -v '^ocfweb==' | sed 's/^ocflib==.*/ocflib/' > requirements.txt

builddeb: autoversion
	dpkg-buildpackage -us -uc -b

.PHONY: autoversion
autoversion:
	date +%Y.%m.%d.%H.%M-git`git rev-list -n1 HEAD | cut -b1-8` > .version
	rm -f debian/changelog
	DEBFULLNAME="Open Computing Facility" DEBEMAIL="help@ocf.berkeley.edu" VISUAL=true \
		dch -v `cat .version` -D stable --no-force-save-on-release \
		--create --package "ocfweb" "Package for Debian."
