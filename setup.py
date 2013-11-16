from distutils.core import setup
from distutils.command.install_lib import install_lib

import shlex
import shutil
import subprocess
import os

SETTINGS_SECRET_FILE = "/root/account_tools_settings.py.secret"


class my_install_lib(install_lib):
    def run(self):
        install_lib.run(self)
        package_location = os.path.join(self.install_dir, "account_tools")

        destination = os.path.join(package_location, "settings.py")
        print "Copying settings file to %s..." % destination,
        shutil.copy(SETTINGS_SECRET_FILE, destination)
        print "done"

        print "Changing owner to account-tools:account-tools...",
        #chown_cmd = "chown -R account-tools:account-tools %s" % package_location
        chown_cmd = "chown -R account-tools:account-tools /var/www/account_tools"
        subprocess.call(shlex.split(chown_cmd))
        print "done"

        print "Chmod go-rwx...",
        chmod_cmd = "chmod -R go-rwx %s" % package_location
        subprocess.call(shlex.split(chmod_cmd))
        print "done"

setup(
    name="account_tools",
    packages=[
        "account_tools",
        "account_tools.approve",
        "account_tools.calnet",
        "account_tools.chpass",
        "account_tools.cmds",
        "account_tools.vhost",
        "account_tools.ocf",
        "account_tools.ocf.validators",
        "account_tools.recaptcha"
    ],
    package_data={
        'account_tools.approve': ['reserved_names.txt'],
        'account_tools': ['templates/*.html'],
    },
    data_files=[
        ('/var/www/account_tools', [
            'public_html/account_tools/.htaccess',
            'public_html/account_tools/account_tools.fcgi'
        ])
    ],
    cmdclass={
        "install_lib": my_install_lib
    },
    version="0.0.1",
    description="OCF account manage Django app",
    author="Kenny Do",
    author_email="kedo@ocf.berkeley.edu",
    url="http://secure.ocf.berkeley.edu/account_tools",
    keywords=["ocf", "account", "password"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration"
        ],
)
