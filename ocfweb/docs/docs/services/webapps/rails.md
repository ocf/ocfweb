[[!meta title="Ruby on Rails"]]

**Note: This document only applies to student groups with virtual hosts who
have applied for apphosting. For normal user accounts or for groups without
apphosting, you'll want to host with FastCGI instead. See our instructions for
that [[here|doc services/web/rails]].**

You will want to deploy your application using [RVM][rvm] so that you can easily
install and manage dependencies and versions.

## Setting up RVM

1. Create a directory for your app to live in:

       mkdir -p ~/myapp
       cd ~/myapp

2. Install RVM in your home directory. Note that `rvm` is terrible and will
   modify your shell config files without asking, but that's probably what you
   want, since it will make using and managing Ruby/Rails easier.

   Go find [the RVM commands][rvm] appropriate for your app, and copy the
   lines straight into your shell to install it. In general this is a bad way
   to install things, but it only has to be done once. At the time of writing,
   it looks like this:

       gpg2 --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3
       curl -sSL https://get.rvm.io | bash -s stable

   Go ahead and run it, and source `rvm`:

       . ~/.rvm/scripts/rvm

3. Install whatever version of Ruby you want. (Newer is better).

       rvm install ruby-2.4.0
       rvm use ruby-2.4.0

4. Copy your code to `~/myapp/src` or similar, and install any dependencies
   using `bundle install` (or `gem` manually, if you aren't using bundler).

   This will download and build whatever gems you have in your `Gemfile`. We've
   tried to install all the headers (dev packages) needed for building common
   gems, but if building a gem fails due to a missing header, just [[send us an
   email|doc contact]] so we can add it.

## Installing unicorn

We recommend using unicorn to serve your application. After setting up RVM, add
a few lines to your app's `Gemfile` (or add a single line if you already have a
`:production` group):

    group :production do
      gem 'unicorn'
    end

and run `bundle install` to install it, as with any new gems.

## Preparing your app to be supervised

Create a file at `~/myapp/run` with content like:

    #!/bin/bash -e
    . ~/.rvm/scripts/rvm
    cd ~/myapp/src
    RAILS_ENV=production \
          exec ~/.rvm/gems/ruby-2.4.0/bin/unicorn_rails \
          -l /srv/apps/$(whoami)/$(whoami).sock

Replace `~/myapp/src` with the path to your app (make sure the path is
correct for the version of Ruby you are using), then make `run` executable:

    chmod +x ~/myapp/run

Test executing the `run` script. You should be able to access your website while
running it (or see any errors in your terminal).

Some things to keep in mind:

* You may need to migrate your database first.
* Make sure you've set secret keys for the app and any gems that need them
  (e.g. devise).
* Static file serving is off by default in production, but you'll want to turn
  it on: set both `config.assets.compile` and `config.serve_static_assets`
  (rails 4.1), `config.serve_static_files` (rails 4.2), or
  `config.public_file_server.enabled` (rails 5) to true in
  `config/environments/production.rb`.

## Supervise your app with systemd

Cool, your app works. [[Set up systemd|doc services/webapps#supervise]] to
supervise your app (so that it starts and restarts automatically).

## Suggestions/improvements?

If you have a better way to host Rails-based apps on the app server (or a
suggestion for how we could improve this documentation), [[send us an email|doc
contact]]!

[rvm]: https://rvm.io/
