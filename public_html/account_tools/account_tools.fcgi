#!/usr/bin/env python
import sys, os

projects_location = "/usr/local/www/django_projects/lib/python"
project_location = os.path.join(projects_location, "account_tools")

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
