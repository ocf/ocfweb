from setuptools import find_packages
from setuptools import setup

with open('.version') as f:
    VERSION = f.readline().strip()

setup(
    name='atool',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    url='https://www.ocf.berkeley.edu/',
    author='Open Computing Facility',
    author_email='help@ocf.berkeley.edu',
    install_requires=[
        'celery[redis]',
        'django',
        'gunicorn',
        'ocflib',
    ],
)
