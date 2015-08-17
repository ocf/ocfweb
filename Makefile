SRC = atool

check: autoversion
	pre-commit run --all-files

dev:
	$(SRC)/manage.py runserver 127.0.0.1:8000

builddeb: autoversion
	dpkg-buildpackage -us -uc -b

autoversion:
	date +%Y.%m.%d.%H.%M-git`git rev-list -n1 HEAD | cut -b1-8` > .version
	rm -f debian/changelog
	DEBFULLNAME="Open Computing Facility" DEBEMAIL="help@ocf.berkeley.edu" VISUAL=true \
		dch -v `cat .version` -D stable --no-force-save-on-release \
		--create --package "ocf-atool" "Package for Debian."

clean:
	rm -rf debian/ocf-atool debian/*.debhelper atool.egg-info debian/*.log debian/ocf-atool.substvars .tox

update-requirements:
	$(eval TMP := $(shell mktemp -d))
	virtualenv -p python3 $(TMP)
	. $(TMP)/bin/activate && \
		pip install --upgrade pip && \
		pip install . && \
		pip freeze | grep -v '^atool==' | sed 's/^ocflib==.*/ocflib/' > requirements.txt
