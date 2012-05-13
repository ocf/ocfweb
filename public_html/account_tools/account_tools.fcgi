#!/usr/bin/env python
import sys, os
import account_tools

sys.path.insert(0, account_tools.__path__[0])

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "account_tools.settings"
os.environ['PYTHON_EGG_CACHE'] = '/var/tmp/egg_cache'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
