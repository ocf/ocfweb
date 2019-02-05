[[!meta title="Django"]]

**Note: These instructions are primarily intended for individual user accounts.
If you are using a group account, you may wish to consider
[[apphosting|doc services/webapps]] instead.**

Django is a popular web framework for Python applications. At the OCF, you can
host it using our regular web hosting, though for groups with virtual hosting,
we strongly recommend instead using our [[application hosting service|doc
services/webapps]] instead, as it provides a first-class solution for webapps.

## Running a Django app

The steps below assume you have already created a Django application. If you
haven't, take a look at [the Django documentation][django-docs] for help with
that.

1. Copy your Django application to your OCF account. For example, you can use
   `scp` to upload it, or if you're using source control, clone it using `git`
   (or another tool) into your home directory.

   In the steps below, we'll assume you put it at `~/app` in your home
   directory.

2. Inside your project directory, create a virtualenv and install your
   dependencies. For example, to create a Python 3 virtualenv, try:

   ```bash
   user@tsunami:~/app$ virtualenv -p python3 venv
   user@tsunami:~/app$ venv/bin/pip install django
   ```

   You'll want to install at least `django` to start with. If you're using
   other packages, install those too. You can also install from a
   `requirements.txt` file, if you have one.

   For full details on how to use pip, see [the pip documentation][pip-docs].

3. Inside that same virtualenv, install the `flup6` package. You can just
   copy-and-paste the below snippet:

   ```bash
   user@tsunami:~/app$ venv/bin/pip install flup6
   ```

   If you're using a `requirements.txt` file, you might want to add it there as
   well. This part varies by how you're organizing your project.

4. Make a directory under `public_html` to house your application. For example,
   `~/public_html/django`. You can also just use `public_html` directly if
   desired.

5. In the directory you just created, make a file called `run.fcgi` with the file contents:

   ```python
   #!/home/u/us/user/app/venv/bin/python
   import os
   import sys

   sys.path.insert(0, os.path.expanduser('~/app'))
   from flup.server.fcgi import WSGIServer

     # Replace "djangoapp" below with your application name
   from djangoapp import wsgi
   if __name__ == '__main__':
       WSGIServer(wsgi.application).run()
   ```

   Make sure to replace the first line of `run.fcgi` file with the actual path
   to your project's virtualenv Python. You can find it by running the command
   `readlink -f ~/app/venv/bin/python`.

   Make sure also to replace `from djangoapp` with the name of your Django
   application (that's the name of the directory containing your `wsgi.py`
   file).

6. In the same directory, run `chmod +x run.fcgi`.

7. In the same directory, create another file called `.htaccess` with these contents:

   ```htaccess
   RewriteEngine on
   RewriteBase /
   RewriteCond %{REQUEST_FILENAME} !-f
   # Change "user" and "django" to your username and whatever directory
   # name you made in public_html, respectively.
   RewriteRule ^(.*)$ /~user/django/run.fcgi/$1 [QSA,L]
   ```

Your app should now be accessible! Note that you will likely have to add
`'www.ocf.berkeley.edu'` to the list of `ALLOWED_HOSTS` in your application's
settings.

### Making assets available

While your application may load, things like images, stylesheets and javascript
might still be failing to load. Generally, the best way to get these to load is
to set the following settings in your application:

```python
STATIC_URL = '/~user/app/static/'
STATIC_ROOT = '/home/u/us/user/public_html/django/static'
```

Make sure to change `user` and `app` in `STATIC_URL` to the correct paths, same
with `u/us/user` and `django` in `STATIC_ROOT`.

Then, to generate assets in `STATIC_ROOT`, run `venv/bin/python manage.py
collectstatic` from the root of your application, and your assets will be
copied to the correct location. This should be done after changing your
application or adding/removing static assets.

### Debugging

If you see an error page when trying to load your app, you may find the
webserver's logs useful. You can access them in the following locations:

* error log: `/opt/httpd/error.log` (most useful)
* suexec log: `/opt/httpd/suexec.log` (only useful in rare cases)

Once your app has started running, changes you make to the Python code or
templates won't take effect for a few hours. To apply changes immediately, the
webserver needs to see that the `run.fcgi` file has changed. You can can change
the modification time of the `run.fcgi` file to trigger a restart with the
command:

```bash
user@tsunami:~$ touch ~/public_html/django/run.fcgi
```


[django-docs]: https://docs.djangoproject.com/en/1.11/intro/tutorial01/
[pip-docs]: https://packaging.python.org/tutorials/installing-packages/#installing-from-pypi
