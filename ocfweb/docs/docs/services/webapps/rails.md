[[!meta title="Ruby on Rails"]]

**Note: This document only applies to student groups with virtual hosts who
have applied for apphosting. For normal user accounts or for groups without
apphosting, you'll want to host with FastCGI instead. See our instructions for
that [[here|services/web/rails]].**

You will want to deploy your application using rvm so that you can easily
install and manage dependencies and versions.

## Setting up rvm

1. Create a directory for your app to live in:

       mkdir -p ~/apps/myapp
       cd ~/apps/myapp

2. Install rvm in your home directory. Note that `rvm` is terrible and will
   modify your shell config files without asking. But maybe that's what you
   want?

   Go find [the RVM one-liner][rvm] appropriate for your app, and copy the
   nasty one-liner straight into your shell to install it. At the time of
   writing, it looks like this:

       curl -sSL https://get.rvm.io | bash -s stable

   Go ahead and run it, and source rvm:

       . ~/.rvm/scripts/rvm

3. Install whatever version of Ruby you want.

       rvm install 2.1.2
       rvm use 2.1.2

4. Include gems in your PATH on login (and for the current session):

       echo "export PATH=~/.rvm/gems/ruby-2.1.2/bin:\$PATH" >> ~/.bash_profile
       export PATH=~/.rvm/gems/ruby-2.1.2/bin:$PATH

4. Copy your code to `~/apps/myapp/src` or similar, and install any
   dependencies using `bundle install` (or `gem` manually, if you aren't using
   bundler).

   This will download and build many gems. We've tried to install all the
   headers (dev packages) needed for building common gems, but if building a
   gem fails due to a missing header, just [[send us an email|contact]] so we
   can add it.

## Installing unicorn

We recommend using unicorn to serve your application. After setting up rvm, add a line to you app's Gemfile:

    'unicorn'

and run `bundle install` to install it.

## Preparing your app to be supervised

Create a file at `~/apps/myapp/run` with content like:

    #!/bin/bash -e
    . ~/.rvm/scripts/rvm
    cd ~/apps/myapp/src
    RAILS_ENV=production \
          exec ~/.rvm/gems/ruby-2.1.2/bin/unicorn_rails \
          -l /srv/apps/$USER/$USER.sock

Replace `~/apps/myapp/src` with the path to your app, then make `run`
executable:

    chmod +x ~/apps/myapp/run

Test executing the run script. You should be able to access your website while
running it (or see any errors in your terminal).

Some things to keep in mind:

* You may need to migrate your database first.
* Make sure you've set secret keys for the app and any gems that need them
  (e.g. devise).
* Static file serving is off by default in production, but you'll want to turn
  it on (set both `config.serve_static_assets` and `config.assets.compile` to
  true in `config/environments/production.rb`)

## Supervise your app with daemontools

Cool, your app works. [[Set up daemontools|services/webapps#supervise]] to
supervise your app (so that it starts and restarts automatically).

## Suggestions/improvements?

If you have a better way to host Rails-based apps on the app server (or a
suggestion for how we could improve this documentation),
[[send us an email|contact]]!

[rvm]: https://rvm.io/
