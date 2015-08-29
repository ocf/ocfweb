SRC = website

check:
	pre-commit run --all-files

dev:
	./manage.py runserver 0.0.0.0:8000

# closer to prod
gunicorn:
	gunicorn -b 0.0.0.0:8000 ocfweb.wsgi

scss:
	python setup.py build_sass

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
		pip freeze | grep -v '^ocf-website==' | sed 's/^ocflib==.*/ocflib/' > requirements.txt
