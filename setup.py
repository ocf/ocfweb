from setuptools import find_packages
from setuptools import setup

try:
    with open('.version') as f:
        VERSION = f.readline().strip()
except IOError:
    VERSION = 'unknown'

setup(
    name='ocfweb',
    version=VERSION,
    packages=find_packages(exclude=['debian', 'virtualenv_run']),
    include_package_data=True,
    url='https://www.ocf.berkeley.edu/',
    author='Open Computing Facility',
    author_email='help@ocf.berkeley.edu',
    install_requires=[
        'cached-property',
        # Celery 3.1.19 has a bug with Redis UNIX sockets that breaks ocfweb:
        # https://github.com/celery/celery/issues/2903
        'celery[redis]<3.1.18',
        'django-bootstrap-form',
        'django-ipware',
        'django-mathfilters',
        'django-redis',
        'django>=1.9,<1.9.999',
        'gunicorn',
        'libsass<=0.10.0',
        'lxml',
        'matplotlib',
        'mistune',
        'numpy',
        'ocflib',
        'pycrypto',
        'pygments',
        'python-dateutil',
    ],
    sass_manifests={
        'ocfweb': ('static/scss',),  # XXX: must be tuple
    },
    entry_points={
        'console_scripts': [
            'ocfweb-run-periodic-functions = ocfweb.bin.run_periodic_functions:main',
        ],
    },
)
