from distutils.core import setup
import os

setup(
    name = "account_tools",
    packages = [
        "account_tools",
        "account_tools.approve",
        "account_tools.calnet",
        "account_tools.chpass",
        "account_tools.ocf",
        "account_tools.ocf.validators",
        "account_tools.recaptcha"
    ],
    package_data = {
        'account_tools.approve': ['reserved_names.txt'],
        'account_tools': ['templates/*.html'],
        },
    version = "0.0.1",
    description = "OCF account manage Django app",
    author = "Kenny Do",
    author_email = "kedo@ocf.berkeley.edu",
    url = "http://secure.ocf.berkeley.edu/account_tools",
    keywords = ["ocf", "account", "password"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration"
        ],
)
