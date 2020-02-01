[[!meta title="Flask"]]

**Note: These instructions are primarily intended for individual user accounts.
If you are using a group account, you may wish to consider
[[apphosting|doc services/webapps]] instead.**

[Flask](https://palletsprojects.com/p/flask/) is a popular microframework for
Python web development. Using it on the OCF servers requires only just a little
extra configuration.


## Setting up a Flask project

1. Make a new directory for your flask app in your home directory. You can name
   this whatever you want, but we'll assume you named the directory `app`:

   ```shell
   user@tsunami:~$ mkdir app
   user@tsunami:~$ cd app
   ```

2. Make a virtualenv.  This will allow you to run `pip install` to install any
   python packages that you need that the OCF does not already have. The
   benefit of having a virtualenv is that you can decide the dependencies you
   want, without being tied to the OCF defaults:

   ```shell
   user@tsunami:~/app$ virtualenv -p python3 venv
   user@tsunami:~/app$ venv/bin/pip install flask flup6
   ```

   Feel free to install any other packages you need for your flask app at this
   step too (or later on, that's cool too). If you have an existing flask app
   with a `requirements.txt` file, then run `venv/bin/pip install -r
   requirements.txt` to install dependencies from that.

   For full details on how to use pip, see [the pip documentation][pip-docs].

3. Create a new python file (or directory) for your application logic. In this
   case, we'll create a new directory named `myapp` and make a new file within
   it named `app.py`:

   ```python
   from flask import Flask
   app = Flask(__name__)

   @app.route('/')
   def hello():
       return 'Hello World!'

   if __name__ == '__main__':
       app.run()
   ```

4. Create a new directory in your `~/public_html/` directory for your flask
   application. You can also just put these files directly in `~/public_html`
   if you want your site available directly under
   `https://www.ocf.berkeley.edu/~user` and you don't have any other sites:

   ```shell
   user@tsunami:~$ mkdir ~/public_html/flask
   ```

   For example, this path above will make your site available at
   `https://www.ocf.berkeley.edu/~user/flask`.

5. Create `~/public_html/flask/.htaccess` with these contents:

   ```apacheconf
   RewriteEngine On
   RewriteBase /
   RewriteCond %{REQUEST_FILENAME} !-f
   # Change "user" and "flask" to your username and whatever directory
   # name you made in public_html, respectively
   RewriteRule ^(.*)$ /~user/flask/run.fcgi/$1 [QSA,L]
   ```

6. Create `~/public_html/flask/run.fcgi` with these contents:

   ```python
   #!/home/u/us/user/app/venv/bin/python
   import os
   import sys

   sys.path.insert(0, os.path.expanduser('~/app'))
   from flup.server.fcgi import WSGIServer
   from myapp.app import app

   if __name__ == '__main__':
       WSGIServer(app).run()
   ```

   Make sure to replace the first line of `run.fcgi` file with the actual path
   to your project's virtualenv Python. You can find it by running the command
   `readlink -f ~/app/venv/bin/python`.

   Make sure to also replace `~/app` (if you have a different path in your home
   directory) and `from myapp.app` with the name of your Flask application that
   you selected before (we used `myapp` and `app.py` but you can use whatever
   you want).

7. Make the `run.fcgi` file you just created executable with:

   ```bash
   user@tsunami:~$ chmod +x ~/public_html/flask/run.fcgi
   ```

8. Once your app has started running, changes you make to the Python code or
   templates won't take effect for a few hours. To apply changes immediately,
   the webserver needs to see that the `run.fcgi` file has changed. You can can
   change the modification time of the `run.fcgi` file to trigger a restart
   with the command:

   ```bash
   user@tsunami:~$ touch ~/public_html/flask/run.fcgi
   ```

### Debugging

If you see an error page when trying to load your app, you may find the
webserver's logs useful. You can access them in the following locations:

* error log: `/opt/httpd/error.log` (most useful)
* suexec log: `/opt/httpd/suexec.log` (only useful in rare cases)


[pip-docs]: https://packaging.python.org/tutorials/installing-packages/#installing-from-pypi
