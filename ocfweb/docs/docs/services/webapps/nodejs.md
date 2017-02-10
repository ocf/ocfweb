[[!meta title="Node.js"]]

**Note: This document only applies to student groups with virtual hosts who
have applied for apphosting. For normal user accounts or for groups without
apphosting, you'll want to host with FastCGI instead.**

You will want to deploy your application using nvm so that you can easily
install and manage dependencies and versions.

## Setting up nvm

1. Create a directory for your app to live in:

       mkdir -p ~/myapp
       cd ~/myapp

2. Install nvm in your home directory. Note that `nvm` is terrible and will
   modify your shell config files without asking. But maybe that's what you
   want?

   Go find the latest version from [the NVM GitHub][nvm-github], and copy the
   nasty one-liner straight into your shell to install it. At the time of
   writing, it looks like this:

       curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh | bash

   Go ahead and run it, and close/re-open your terminal as it suggests.

3. Install whatever version of Node.js you want.

       nvm install 6
       nvm alias default 6

4. Copy your code to `~/myapp/src` or similar, and install any dependencies
   using `npm`.

## Preparing your app to be supervised

Create a file at `~/myapp/run` with content like:

    #!/bin/bash -e
    USER="$(whoami)"
    [ -e "/srv/apps/$USER/$USER.sock" ] && rm "/srv/apps/$USER/$USER.sock"
    umask 0

    . ~/.nvm/nvm.sh
    NODE_ENV=production PORT="/srv/apps/$USER/$USER.sock" \
        exec ~/myapp/src/bin/www

Replace `~/myapp/src/bin/www` with the path to your app, then make `run`
executable:

    chmod +x ~/myapp/run

Test executing the run script. You should be able to access your website while
running it (or see any errors in your terminal).

## Supervise your app with systemd

Cool, your app works. [[Set up systemd|doc services/webapps#supervise]] to
supervise your app (so that it starts and restarts automatically).

## Suggestions/improvements?

If you have a better way to host Node.js-based apps on the app server (or a
suggestion for how we could improve this documentation), [[send us an email|doc
contact]]!

[nvm-github]: https://github.com/creationix/nvm
