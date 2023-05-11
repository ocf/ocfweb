BIN := venv/bin
PYTHON := $(BIN)/python
SHELL := /bin/bash
RANDOM_PORT := $(shell expr $$(( 8000 + (`id -u` % 1000) )))
LISTEN_IP := 0.0.0.0
DOCKER_REPO ?= docker-push.ocf.berkeley.edu/
DOCKER_REVISION ?= testing-$(USER)
DOCKER_TAG_BASE = ocfweb-base-$(USER)
DOCKER_TAG_WEB = $(DOCKER_REPO)ocfweb-web:$(DOCKER_REVISION)
DOCKER_TAG_WORKER = $(DOCKER_REPO)ocfweb-worker:$(DOCKER_REVISION)
DOCKER_TAG_STATIC = $(DOCKER_REPO)ocfweb-static:$(DOCKER_REVISION)

.PHONY: test
test: export OCFWEB_TESTING ?= 1
test: venv mypy
	$(BIN)/py.test -v tests/
	$(BIN)/pre-commit run --all-files

.PHONY: mypy
mypy: venv
	$(BIN)/mypy -p ocfweb

.PHONY: Dockerfile.%
Dockerfile.%: Dockerfile.%.in
	sed 's/{tag}/$(DOCKER_TAG_BASE)/g' "$<" > "$@"

.PHONY: cook-image
cook-image: Dockerfile.web Dockerfile.worker Dockerfile.static
	$(eval OCFLIB_VERSION := ==$(shell curl https://pypi.org/pypi/ocflib/json | jq -r .info.version))
	docker build --pull --build-arg ocflib_version=$(OCFLIB_VERSION) -t $(DOCKER_TAG_BASE) .
	docker build -t $(DOCKER_TAG_WEB) -f Dockerfile.web .
	docker build -t $(DOCKER_TAG_WORKER) -f Dockerfile.worker .
	docker build -t $(DOCKER_TAG_STATIC) -f Dockerfile.static .

.PHONY: push-image
push-image:
	docker push $(DOCKER_TAG_WEB)
	docker push $(DOCKER_TAG_WORKER)
	docker push $(DOCKER_TAG_STATIC)

.PHONY: dev
dev: venv ocfweb/static/scss/site.scss.css
	@echo -e "\e[1m\e[93mRunning on http://$(shell hostname -f ):$(RANDOM_PORT)/\e[0m"
	$(PYTHON) ./manage.py runserver $(LISTEN_IP):$(RANDOM_PORT)

.PHONY: local-dev
local-dev: LISTEN_IP=127.0.0.1
local-dev: dev

venv: requirements.txt requirements-dev.txt
	python3 ./vendor/venv-update venv= venv -ppython3.9 install= -r requirements.txt -r requirements-dev.txt

.PHONY: install-hooks
install-hooks: venv
	$(BIN)/pre-commit install -f --install-hooks

.PHONY: lint
lint: venv
	$(BIN)/pre-commit run --all-files

.PHONY: clean
clean:
	rm -rf *.egg-info venv

# closer to prod
.PHONY: gunicorn
gunicorn: venv
	@echo "Running on port $(RANDOM_PORT)"
	$(BIN)/gunicorn -b 0.0.0.0:$(RANDOM_PORT) ocfweb.wsgi

# phony because it depends on other files, too many to express
.PHONY: ocfweb/static/scss/site.scss.css
ocfweb/static/scss/site.scss.css: ocfweb/static/scss/site.scss venv
	$(BIN)/pysassc "$<" "$@"

.PHONY: watch-scss
watch-scss: venv
	while :; do \
		make ocfweb/static/scss/site.scss.css; \
		find ocfweb/static -type f -name '*.scss' | \
			inotifywait --fromfile - -e modify; \
	done

.PHONY: update-requirements
update-requirements: venv
	$(BIN)/upgrade-requirements
	sed -i 's/^ocflib==.*/ocflib/' requirements.txt
