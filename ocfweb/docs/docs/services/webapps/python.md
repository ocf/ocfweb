[[!meta title="Python (Django, Flask, etc.)"]]

**Note: This document only applies to student groups with virtual hosts who
have applied for apphosting. For normal user accounts or for groups without
apphosting, you'll want to host with FastCGI instead. See our instructions for
[[Django|doc services/web/django]] or [[Flask|doc services/web/flask]].**

You will want to deploy your application using a virtualenv so that you can
easily install and manage dependencies and versions.

## Setting up a virtualenv

1. Create a directory for your app to live in:

       mkdir -p ~/apps/myapp
       cd ~/apps/myapp

2. Set up a virtualenv:

       virtualenv venv

3. Activate the virtualenv:

       . venv/bin/activate

   You should do this step every time before running your app or managing
   installed packages.

4. Copy your code to `~/apps/myapp/src` or similar, and install any
   dependencies using `pip`.

## Installing gunicorn

We recommend using gunicorn to serve your application. After activating your
virtualenv, install it with `pip install gunicorn`.

Note that you may see a warning about a syntax error. As long as the output
ends in "Successfully installed gunicorn", [it's safe to ignore
this][lol-syntax].

## Preparing your app to be supervised

Create a file at `~/apps/myapp/run` with content like:

    #!/bin/sh -e
    . ~/apps/myapp/venv/bin/activate
    PYTHONPATH=~/apps/myapp/src:$PYTHONPATH \
        exec gunicorn -w 2 -b unix:/srv/apps/$USER/$USER.sock \
        --log-file - main:app

Replace `main:app` with the module containing the app, and name of your app,
then make `run` executable:

    chmod +x ~/apps/myapp/run

Test executing the run script. You should be able to access your website while
running it (or see any errors in your terminal).

## Supervise your app with daemontools

Cool, your app works. [[Set up daemontools|doc services/webapps#supervise]] to
supervise your app (so that it starts and restarts automatically).

### Bonus Gunicorn tip: reloading your app

Gunicorn will reload your app if you send it SIGHUP. You can do that using
daemontools:

    svc -h ~/apps/myapp

## Suggestions/improvements?

If you have a better way to host Python-based apps on the app server (or a
suggestion for how we could improve this documentation),
[[send us an email|doc contact]]!

[lol-syntax]: https://stackoverflow.com/a/25611194
