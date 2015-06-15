from setuptools import setup, find_packages

VERSION = 4

setup(
    name='atool',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    url='https://www.ocf.berkeley.edu/',
    author='Open Computing Facility',
    author_email='help@ocf.berkeley.edu',
)
