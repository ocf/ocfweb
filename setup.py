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
        'cachetools',
        'django>=1.8,<1.8.999',
        'gunicorn',
        'libsass',
        'lxml',
        'mistune',
        'ocflib',
        'pygments',
        'python-dateutil',
    ],
    sass_manifests={
        'ocfweb': ('static/scss',),
    },
)
