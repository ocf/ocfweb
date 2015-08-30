[[!meta title="Ruby on Rails"]]


Ruby on Rails is a popular web framework for Ruby applications.

## Installing Rails 4

OCF servers currently run the following:

* Ruby 1.9
* Rails 3.2.6

If you'd like, you can install Rails 4 in your home directory using `gem`.  The
installed version of Ruby should be sufficient. The following steps, which
should all take place over [[SSH|doc services/shell]], will set up a gem directory
inside your home directory and installs Rails.

1. Set up relevant environment variables on login:

       echo "export PATH=~/.gem/ruby/1.9.1/bin:\$PATH" >> ~/.bash_profile
       echo "export GEM_HOME=~/.gem/ruby/1.9.1/gems" >> ~/.bash_profile
       echo "export GEM_PATH=~/.gem/ruby/1.9.1" >> ~/.bash_profile

2. Create a `gemrc` file specifying default installation optipns:

       echo "gem: --user-install" > ~/.gemrc

3. Disconnect and reconnect to SSH, or re-source your profile:

       . ~/.bash_profile

4. Install `rails` via `gem`:

       gem install --no-rdoc --no-ri rails

   This may take some time.

5. Verify that Rails is installed:

       rails -v

   You should see output indicating the new Rails version. If you see an old
   version (like 3.2.6), your PATH is probably wrong. Make sure you followed step
   1 and try reconnecting to SSH.

## Creating a New Application

To create a new Rails application, use the `rails` command-line interface. For example,
to create an application called `foo` in your home directory, run the command:

    rails new foo

This may take some time.

## Hosting Your Application

OCF allows hosting of Rails applications via FastCGI. This requires you to install the
`fcgi` gem and create a FastCGI wrapper script.

### Install `fcgi` gem

1. Make sure the line `gem 'fcgi'` appears somewhere in your project's
   `Gemfile` (located at the root of the project).

2. Run `bundle install` from the root of your project to update installed gems.
   This will ensure that the `fcgi` gem is installed.

### Create FastCGI wrapper script

To host your application, create a file called `dispatch.fcgi` in your web root
(`~/public_html/`) based on the following template:

    #!/usr/bin/ruby
    ENV['HOME'] = `/bin/bash -c "echo ~"`
    ENV['GEM_HOME'] = ENV['HOME'] + '/.gem/ruby/1.9.1/gems'
    ENV['GEM_PATH'] = ENV['HOME'] + '/.gem/ruby/1.9.1'

    APP_PATH = ENV['HOME'] + '/foo'

    require_relative APP_PATH + '/config/environment'

    class Rack::PathInfoRewriter
      def initialize(app)
        @app = app
      end

      def call(env)
        env.delete('SCRIPT_NAME')
        parts = env['REQUEST_URI'].split('?')
        env['PATH_INFO'] = parts[0]
        env['QUERY_STRING'] = parts[1].to_s
        @app.call(env)
      end
    end

    Rack::Handler::FastCGI.run Rack::PathInfoRewriter.new(Foo::Application)

Be sure to adjust:

* The path to your application (`APP_PATH` variable)
* The name of your application (last line). Change `Foo::Application` to
  `MyApp::Application` where `MyApp` is the name of your application.

Once you've added the `dispatch.fcgi` file, mark it as executable:

    chmod +x dispatch.fcgi

### Rewrite requests to the FastCGI wrapper

Create a file called `.htaccess` in your web root (or a subdirectory)
containing the following lines:

    RewriteEngine On
    RewriteBase /
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteRule ^(.*)$ /~user/dispatch.fcgi [QSA,L]

Be sure to replace `user` with your username.

### Debugging

If you see an error page when trying to load your app, you may find the
webserver's logs useful. You can access them via SSH in the following
locations:

* error log: `/opt/httpd/error.log` (most useful)
* suexec log: `/opt/httpd/httpd-suexec.log` (only useful in rare cases)

Once your app has started running, changes you make to the Ruby code or
templates won't take effect for a few hours. To apply changes immediately, you
can touch the dispatch.fcgi file with the command:

     $ touch dispatch.fcgi
