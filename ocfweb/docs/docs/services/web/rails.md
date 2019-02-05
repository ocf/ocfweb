[[!meta title="Ruby on Rails"]]

**Note: These instructions are primarily intended for individual user accounts.
If you are using a group account, you may wish to consider
[[apphosting|doc services/webapps]] instead.**

Ruby on Rails is a popular web framework for Ruby applications.

## Creating a New Application

To create a new Rails application, use the `rails` command-line interface. For
example, to create an application called `foo` in your home directory, run the
command:

```bash
user@tsunami:~$ rails new foo
```

This may take some time.

## Hosting Your Application

OCF allows hosting of Rails applications via FastCGI. This requires you to
install the `fcgi` gem and create a FastCGI wrapper script.

### Install `fcgi` gem

1. Make sure the line `gem 'fcgi'` appears somewhere in your project's
   `Gemfile` (located at the root of the project).

2. Run `bundle install --path bundle` from the root of your project to install
   bundled gems. This will also ensure that the `fcgi` gem is installed. You'll
   want to specify `--path bundle` so that bundler installs your gems to a
   local directory to your app and not system-wide. You'll also likely want to
   add the new `bundle` directory to your `.gitignore` if you are using git for
   version control.

### Create FastCGI wrapper script

To host your application, create a file called `dispatch.fcgi` in your web root
(`~/public_html/`) based on the following template:

```ruby
#!/usr/bin/ruby
require 'etc'

APP_PATH = Etc.getpwuid.dir + '/foo'
ENV['GEM_HOME'] = APP_PATH + '/bundle/ruby/2.3.0/gems'
ENV['GEM_PATH'] = APP_PATH + '/bundle/ruby/2.3.0'

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

app, options = Rack::Builder.parse_file(APP_PATH + '/config.ru')
wrappedApp = Rack::Builder.new do
  use Rack::ShowExceptions
  use Rack::PathInfoRewriter
  run app
end

Rack::Handler::FastCGI.run wrappedApp
```

Be sure to adjust the path to your application near the top of the file
(the `APP_PATH` variable)

Once you've added the `dispatch.fcgi` file, mark it as executable:

```bash
user@tsunami:~/public_html$ chmod +x dispatch.fcgi
```

### Rewrite requests to the FastCGI wrapper

Create a file called `.htaccess` in your web root (or a subdirectory)
containing the following lines:

```htaccess
RewriteEngine On
RewriteBase /
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ /~user/rails/dispatch.fcgi [QSA,L]
```

Be sure to change `user` and `rails` to your username and whatever directory
name you made in `public_html`, respectively. (or remove `rails` if not inside
a separate directory)

### Rewriting asset and route paths

One issue you may run into is an error like `No route matches [GET] "/~user"`.
To fix an issue like this, the best method is to edit `config/routes.rb` in
your application and add a `scope` block around all your routes matching the
path you are using. For instance, if your site is at
`https://www.ocf.berkeley.edu/~user` then convert your routes from something like this:

```ruby
MyApp::Application.routes.draw do
  resources :users

  [...]
end
```

to something like this:

```ruby
MyApp::Application.routes.draw do
  scope "~user" do
    resources :users

    [...]
  end
end
```

This will make your application able to route all your existing routes
correctly. If your site is at something like
`https://www.ocf.berkeley.edu/~user/rails` then use `~user/rails` in the scope
block instead. However, assets (images, stylesheets, javascript) may still be
broken. To fix these, add a line like this into your `config/application.rb`
(or under the correct environment in
`config/environments/(development,production).rb` if you want to be more
specific). Note that this has to be inside the `class Application` block:

```ruby
Rails.application.config.assets.prefix = "/~user/asset"
```

Make sure to replace `user` in this example (and in your `config/routes.rb`)
with your username, and add the path you are using for your application if
applicable between `~user` and `~asset`.

### Debugging

If you see an error page when trying to load your app, you may find the
webserver's logs useful. You can access them in the following locations:

* error log: `/opt/httpd/error.log` (most useful)
* suexec log: `/opt/httpd/suexec.log` (only useful in rare cases)

Once your app has started running, changes you make to the Ruby code or
templates won't take effect for a few hours. To apply changes immediately, you
can touch the dispatch.fcgi file with the command:

```bash
user@tsunami:~/public_html$ touch dispatch.fcgi
```
