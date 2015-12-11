BIN := virtualenv_run/bin
PYTHON := $(BIN)/python
SHELL := /bin/bash
RANDOM_PORT := $(shell expr $$(( 8000 + (`id -u` % 1000) )))

.PHONY: test
test: virtualenv_run/
	$(BIN)/coverage erase
	COVERAGE_PROCESS_START=$(PWD)/.coveragerc \
		$(BIN)/py.test -v tests/
	$(BIN)/coverage combine
	$(BIN)/coverage report
	$(BIN)/pre-commit run --all-files

# first set COVERALLS_REPO_TOKEN=<repo token> environment variable
.PHONY: coveralls
coveralls: virtualenv_run/ test
	$(BIN)/coveralls

.PHONY: dev
dev: virtualenv_run/ scss
	@echo -e "\e[1m\e[93mRunning on http://$(shell hostname -f ):$(RANDOM_PORT)/\e[0m"
	$(PYTHON) ./manage.py runserver 0.0.0.0:$(RANDOM_PORT)

virtualenv_run/: requirements.txt requirements-dev.txt
	python ./bin/venv-update -ppython3 virtualenv_run requirements.txt requirements-dev.txt

.PHONY: clean
clean:
	rm -rf *.egg-info
	rm -rf virtualenv_run

# closer to prod
.PHONY: gunicorn
gunicorn: virtualenv_run/
	@echo "Running on port $(RANDOM_PORT)"
	$(BIN)/gunicorn -b 0.0.0.0:$(RANDOM_PORT) ocfweb.wsgi

.PHONY: scss
scss: virtualenv_run/
	$(PYTHON) setup.py build_sass

.PHONY: watch-scss
watch-scss: scss virtualenv_run
	while :; do \
		find ocfweb/static -type f -name '*.scss' | \
			inotifywait --fromfile - -e modify; \
			$(PYTHON) setup.py build_sass; \
	done

.PHONY: update-requirements
update-requirements:
	$(eval TMP := $(shell mktemp -d))
	awk '/^\s*install_requires=\[$$/,/^\s*],$$/' setup.py | \
		tail -n +2 | head -n -1 | \
		grep -oE "'[^']+'" | \
		cut -c 2- | rev | cut -c 2- | rev > $(TMP)/requirements.txt
	python ./bin/venv-update -ppython3 $(TMP)/venv $(TMP)/requirements.txt
	. $(TMP)/venv/bin/activate && \
		pip freeze | sort | grep -vE '^(wheel|ocfweb)==' | sed 's/^ocflib==.*/ocflib/' > requirements.txt
	rm -rf $(TMP)

.PHONY: builddeb
builddeb: autoversion
	dpkg-buildpackage -us -uc -b

.PHONY: autoversion
autoversion:
	date +%Y.%m.%d.%H.%M-git`git rev-list -n1 HEAD | cut -b1-8` > .version
	rm -f debian/changelog
	DEBFULLNAME="Open Computing Facility" DEBEMAIL="help@ocf.berkeley.edu" VISUAL=true \
		dch -v `cat .version` -D stable --no-force-save-on-release \
		--create --package "ocfweb" "Package for Debian."
