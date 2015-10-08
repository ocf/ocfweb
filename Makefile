BIN := virtualenv_run/bin
PYTHON := $(BIN)/python
SHELL := /bin/bash
RANDOM_PORT := $(shell expr $$(( 8000 + (`id -u` % 1000) )))

.PHONY: check dev venv clean lint test gunicorn

check: lint test

lint: venv
	$(BIN)/pre-commit run --all-files

test: venv
	$(BIN)/py.test -v tests/
	$(BIN)/pre-commit run --all-files

dev: venv scss
	@echo -e "\e[1m\e[93mRunning on http://$(shell hostname -f ):$(RANDOM_PORT)/\e[0m"
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

watch-scss: scss venv
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
