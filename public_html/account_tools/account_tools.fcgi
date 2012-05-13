#!/usr/bin/env python
import sys, os
import account_tools

os.environ["DJANGO_SETTINGS_MODULE"] = "account_tools.settings"
os.environ['PYTHON_EGG_CACHE'] = '/usr/local/www/django_projects/egg_cache'

os.chdir(account_tools.__path__[0])
sys.path.insert(0, account_tools.__path__[0])

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

