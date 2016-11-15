[[!meta title="Django"]]

Django is a popular web framework for Python applications.


## Starting a Django project

The necessary scripts for you to create Django projects are installed on our
login server, _ssh.ocf.berkeley.edu_.

1.   First, you will want to create a directory to store all of your Django
     projects. This directory should not be in your *public_html* directory.

         tsunami$ mkdir ~/projects

1.   Go into the directory you just created:

         tsunami$ cd ~/projects

1.   Create a new Django project. For this example, the project name will be
     "hatsune". You will want to stick with Python-friendly package and module
     names, as detailed in [PEP
     8](https://www.python.org/dev/peps/pep-0008/#package-and-module-names).

         tsunami$ django-admin startproject hatsune

1.   Go into the project directory you just created and edit the settings.py
     file with the necessary information:

         tsunami$ cd hatsune
         tsunami$ vim settings.py

1.   Change the permissions of the settings.py file, since it might have
     sensitive information like your database password!

         tsunami$ chmod go-rwx settings.py

1.   Create an app, edit it, and so on:

         tsunami$ django-admin startapp miku
         tsunami$ vim miku/views.py
         ...
         tsunami$ vim urls.py

1.    Make a directory in your ~/public_html directory:

        tsunami$ mkdir ~/public_html/hatsune

1.    Go into the directory you just created, and create two files: *.htaccess*
      (note the dot), and *run.fcgi*.

* .htaccess:

      RewriteEngine On
      RewriteBase /
      RewriteCond %{REQUEST_FILENAME} !-f
      # Change "username" and "hatsune" to your username and whatever directory name you made in public_html, respectively
      RewriteRule ^(.*)$ /~username/hatsune/run.fcgi/$1 [QSA,L]

* run.fcgi:

      #!/usr/bin/env python
      import sys, os

      # Change this path to reflect the real directory where your django-project lives
      projects_location = "/home/k/ke/kedo/django"
      project_name = "hatsune"

      sys.path.insert(0, projects_location)
      sys.path.insert(1, os.path.join(projects_location, project_name))
      os.chdir(projects_location)

      os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % project_name

      from django.core.servers.fastcgi import runfastcgi
      runfastcgi(method="threaded", daemonize="false")

1.   Make the *run.fcgi* file you just created executable:

         tsunami$ chmod a+x run.fcgi

1. Double check that your *settings.py* file is *not* readable by any other
   users, and try not to leave DEBUG set to True in your settings.py. Also note
   that paths are very finicky for Django (and Python) projects, and incorrect
   paths will likely be the source of any problems.

1. Once your app has started running, changes you make to the Python code or
   templates won't take effect for a few hours. To apply changes immediately,
   you can touch the run.fcgi file with the command:

       tsunami$ touch run.fcgi
