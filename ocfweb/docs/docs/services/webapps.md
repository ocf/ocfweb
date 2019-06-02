[[!meta title="Web application hosting"]]

**Note: This document only applies to student groups with virtual hosts who
have applied for apphosting. For normal user accounts or for groups without
apphosting, you'll want to host with FastCGI instead.**


## Introduction

All accounts include our [[standard web hosting|doc services/web]], which is
suitable for static content, PHP (WordPress, Joomla, etc.), and CGI/FastCGI.
For student groups wishing to host more advanced web apps with the OCF (Django,
Flask, Rails, Node.js, etc.), we offer a separate hosting platform which
provides more flexibility.

## App hosting eligibility

App hosting is *only available for student groups with [[virtually-hosting
domain names|doc services/vhost]]* (either group.berkeley.edu, or your own
separately-purchased domain name). If you don't already have a virtual host and
want to use app hosting, see below for instructions; please don't fill out a
virtual host request form.

## Requesting app hosting

To request app hosting, you need to first [[create an OCF group account|doc
membership]]. Once you have an account, email `hostmaster@ocf.berkeley.edu`
with at least the following information:

* Group's account name
* Group's current website, if any (even if not hosted by OCF)
* Desired domain name for the app (either group.berkeley.edu, or your own
  domain)
* The technologies/languages your site is built on

## Requirements for virtually-hosted apps

All [[normal requirements for virtual hosts|doc services/vhost]] apply. In
particular, be sure you are in compliance with the university student group
disclaimer policy, and that your website features a "Hosted by OCF" banner.

## Technical documentation

You can host basically any kind of web application that can bind to a socket.
We provide suggested deployment instructions for some popular web applications
below, but if you know what you're doing, you needn't follow them.

### Connecting to the application server

We provide a separate server (currently named `vampires`), for hosting
applications. **You should connect to this server**, not to the public login
server.

You connect to this server via SSH using your normal OCF account name and
password.

* **Host:** apphost.ocf.berkeley.edu
* **Port:** 22

If your login is refused (but you *can* log in to `ssh.ocf.berkeley.edu`), your
account probably isn't configured yet. Contact us (see above) to request app
hosting on your account.

### Routing traffic to your app

Our application server uses a reverse proxy to route traffic to UNIX sockets
located at `/srv/apps/username/username.sock`. Your application should bind to
that socket; basically any server can be configured to bind to a UNIX socket
instead of a port, so do that.

We provide some example setups below.

### Supervising and starting your app    {supervise}

**Make sure you do these steps on the application server.** If you start your
app on tsunami, the public login server, it won't work.

We may restart the application server as part of regular maintenance, and
you'll want your app to start again when we do. You'll also want your app to
automatically restart if it crashes.

We highly recommend to use systemd to supervise your app. Our recommended setup
is:

1. Create a directory for your app `~/myapp`.

2. Place a startup script at `~/myapp/run`. Your script should end by `exec`ing
   the server process. If you followed one of the guides for [[Node.js|doc
   services/webapps/nodejs]], [[Rails|doc services/webapps/rails]], or
   [[Django|doc services/webapps/python]], you've already created this file, so
   can move on to the next step.

   Otherwise, an example would be:

       #!/bin/sh -e
       exec ~/myapp/run-server

   Your server should run in the *foreground* (it should not daemonize), and
   the `run` script should end with an `exec` line so that signals are sent to
   the server (and not to the shell that started it).

   Once you've written the script, make it executable (`chmod +x ~/myapp/run`).
   Test it by executing it in your terminal before moving on; it will be easier
   to debug problems.

3. Write a systemd service file so your app will be supervised on startup. Save
   the following to the file `~/.config/systemd/user/myapp.service`:

       [Unit]
       Description={YOUR GROUP NAME} Webapp
       ConditionHost=vampires

       [Install]
       WantedBy=default.target

       [Service]
       ExecStart=/home/{U}/{UU}/{USERNAME}/myapp/run
       Restart=always

   Make sure to replace `{YOUR GROUP NAME}` above with your actual group name,
   and also replace `{U}` with the first letter of your username, `{UU}` with
   the first two letters of your username, and `{USERNAME}` with your username.

4. Tell systemd to start your app on startup, by running `systemctl --user
   enable myapp`.

5. You'll need to start your app manually once (on future reboots, it will be
   started for you). To do that, run `systemctl --user start myapp`.

To control your app, you can use the `systemctl` tool. See `man systemctl` for
full details. In summary,

* **Restart an app.** `systemctl --user restart myapp`
* **Bring an app offline.** `systemctl --user stop myapp`
* **Bring an app back online.** `systemctl --user start myapp`
* **Check the status of an app.** `systemctl --user status myapp`

Your app's standard output and error streams are sent to systemd's journal (by
default). You can view them using `journalctl --user -n`. See `man journalctl`
for more options.

## Frequently asked questions
### Can you install a package on the app server?

Probably. [[Send us an email|doc contact]], and be sure to provide the name of
the [Debian package][dpkg] you want us to install. Keep in mind we'll probably
be installing the stable version of the package, so it might be old.

You might prefer to install the package locally. See below.

### This package is 7 years old. Can you update it?

Probably not. Our servers run Debian stable, so it's expected that system
packages aren't current (indeed, they're often a few years old). We almost
never make exceptions or install backported packages.

For developing and deploying your app, you should almost certainly be using
your platform's version manager (rvm, virtualenv, nvm, gvm, etc.). This will
allow you to run the exact versions you want, and install any necessary
dependencies, all without coordinating with us (or forcing the rest of our
users to switch versions).

The pages above provide instructions on doing this with popular programming
languages.

### How do I get a database for my application?

A [[MySQL database|doc services/mysql]] is included with your OCF account. You
should probably just use that. We're *not* going to set up a different database
for you (you could install one in your home directory if you *really* want to).

### I'm running my app on port 3000 but I can't access it.

The app server is behind a firewall; you won't be able to access most ports
from outside of the OCF. You could come work from [[the lab|doc services/lab]],
or forward the port over SSH from elsewhere.

[dpkg]: https://www.debian.org/distrib/packages#search_packages
