#!/usr/bin/env python
import sys, os
sys.path.insert(0, "/var/www/account_tools/lib/python2.7/site-packages")
sys.path.insert(1, "/var/www/account_tools/lib/python2.7/site-packages/account_tools")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "account_tools.settings"
os.environ['PYTHON_EGG_CACHE'] = '/var/tmp/egg_cache'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
