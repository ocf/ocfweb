#!/usr/bin/env python
import sys, os
import account_tools

projects_location = os.path.join(account_tools.__path__[0], os.path.pardir)
project_location = "%s/account_tools" % projects_location

# Add a custom Python path.
sys.path.insert(0, projects_location)
sys.path.insert(1, project_location)
# Switch to the directory of your project. (Optional.)
os.chdir(project_location)

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "account_tools.settings"
os.environ['PYTHON_EGG_CACHE'] = '/var/tmp/egg_cache'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
