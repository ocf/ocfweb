[[!meta title="Flask"]]

Flask is a popular microframework for Python web development. Using it on the
OCF servers requires only just a little extra configuration.


## Starting a Flask project    {starting}

1.    Make a directory in your ~/public_html directory:

          $ mkdir ~/public_html/flasky

1.    Go into the directory you just created, and create two files: *.htaccess*
      (note the dot), and *run.fcgi*.

* .htaccess:

      RewriteEngine On
      RewriteBase /
      RewriteCond %{REQUEST_FILENAME} !-f
      # Change "username" and "flasky" to your username and whatever directory name you made in public_html, respectively
      RewriteRule ^(.*)$ /~username/flasky/run.fcgi/$1 [QSA,L]

* run.fcgi:

      #!/usr/bin/env python
      from flup.server.fcgi import WSGIServer
      from flaskyapplication import app

      if __name__ == '__main__':
          WSGIServer(app).run()

1.    Either add your application as a module in this folder or a subdirectory
      that will be treated as a python package:

* Case 1:

      /flaskyapplication.py
      /run.fcgi

* Case 2:

      /flaskyapplication
          /__init__.py
      /run.fcgi

1.   Write your application logic inside the module or package:

     ```
     from flask import Flask
     app = Flask(__name__)

     @app.route('/')
     def hello_world():
         return 'Hello World!'

     if __name__ == '__main__':
         app.run()
     ```

1. Make the *run.fcgi* file you just created executable:

       $ chmod a+x ~/public_html/flasky/run.fcgi

1. Once your app has started running, changes you make to the Python code or
   templates won't take effect for a few hours. To apply changes immediately,
   you can touch the run.fcgi file with the command:

       $ touch run.fcgi
