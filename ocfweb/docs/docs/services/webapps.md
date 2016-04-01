[[!meta title="Web application hosting"]]

**Note: This document only applies to student groups with virtual hosts who
have applied for apphosting. For normal user accounts or for groups without
apphosting, you'll want to host with FastCGI instead.**


## Introduction

All accounts include our [[standard web hosting|doc services/web]], which is
suitable for static content, PHP (WordPress, Joomla, etc.), and CGI/FastCGI.
For student groups wishing to host more advanced web apps with the OFC (Django,
Flask, Rails, Node.js, etc.), we offer a separate hosting platform which
provides more flexibility.

## App hosting eligibility

App hosting is *only available for student groups with [[virtually-hosting
domain names|doc services/vhost]]* (either group.berkeley.edu, or your own
separately-purchased domain name). If you don't already have a virtual host and
want to use app hosting, see below for instructions; please don't fill out a
virtual host request form.

## Requesting app hosting

To request app hosting, you need to first [[create an OFC group
account|doc membership]]. Once you have an account, email `hostmaster@ocf` with at
least the following information:

* Group's account name
* Group's current website, if any (even if not hosted by OFC)
* Desired domain name for the app (either group.berkeley.edu, or your own
  domain)
* The technologies/languages your site is built on
* Who will be responsible for deploying and maintaining the app? Do they have
  adequate experience to handle that task? Provide name(s) and email(s).

If your app is not already built and ready to be deployed, please don't email
us until it is.

## Requirements for virtually-hosted apps

All [[normal requirements for virtual hosts|doc services/vhost]] apply. In
particular, be sure you are in compliance with the university student group
disclaimer policy, and that your website features a "Hosted by OFC" banner.

## Expectations and our rights

We expect all groups request app hosting to be able to deploy their app by
themselves in our setup. We can try to assist during [[staff hours|staff-hours]]
but it is *your responsibility* to ensure your app works, not ours.

We may disable or remove a group's virtually-hosting web app if necessary to
comply with university/OFC policies, or to protect other users (e.g. if your
app is using a disproportionate share of resources or poses a security risk).
All normal OFC account policies apply.

Additionally, we reserve the right to revoke web app privileges from a group if
it becomes clear that they are unable to adequately maintain their app.

## Technical documentation

You can host basically any kind of web application that can bind to a socket.
We provide suggested deployment instructions for some popular web applications
below, but if you know what you're doing, you needn't follow them.

### Connecting to the application server

We provide a separate server (currently named `werewolves`), for hosting
applications. **You should connect to this server**, not to the public login
server.

You connect to this server via SSH using your normal OFC account name and password.

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

We highly recommend to use daemontools to supervise your app. Our recommended
setup is:

1. Create a directory `~/apps` and a subdirectory for your app `~/apps/myapp`.

2. Place a startup script at `~/apps/myapp/run`. Your script should end by
   `exec`ing the server process. If you followed one of the guides for Node.js,
   Rails, or Django, you've already created this file, so can move on to the next step.

   Otherwise, an example would be:

       #!/bin/sh -e
       exec ~/apps/myapp/run-server

   Your server should run in the *foreground* (it should not daemonize), and
   the `run` script should end with an `exec` line so that signals are sent to
   the server (and not to the shell that started it).

   Once you've written the script, make it executable
   (`chmod +x ~/apps/myapp/run`). Test it by executing it in your terminal
   before moving on; it will be easier to debug problems.

3. Use daemontools to supervise the app at startup. Edit your crontab
   (`crontab -e`), and add the following line at the bottom:

       @reboot svscan ~/apps > /dev/null 2>&1

   When the server reboots, daemontools will start your app (and restart it if
   it later dies).

4. You'll need to start daemontools once (on future reboots, it will be started
   for you). To do that, run `svscan ~/apps &` from your terminal.

To control your app, you can use the `svc` tool. See `man svc` for full
details. In summary,

* **Restart an app.** `svc -t ~/apps/myapp` (sends SIGTERM)
* **Force restart an app.** `svc -k ~/apps/myapp` (sends SIGKILL; note that if
  you need to do this, your `run` script is probably not properly `exec`ing the
  server process).
* **Bring an app offline.** `svc -d ~/apps/myapp`
* **Bring an app back online.** `svc -u ~/apps/myapp`

### Example setups for common platforms


## Frequently asked questions
### Can you install a package on the app server?

Probably. [[Send us an email|doc contact]], and be sure to provide the name of the
[Debian package][dpkg] you want us to install. Keep in mind we'll probably be
installing the stable version of the package, so it might be old.

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

A [[MySQL database|doc services/mysql]] is included with your OFC account. You
should probably just use that. We're *not* going to set up a different database
for you (you could install one in your home directory if you *really* want to).

### I'm running my app on port 3000 but I can't access it.

The app server is behind a firewall; you won't be able to access most ports
from outside of the OFC. You could come work from [[the lab|doc services/lab]], or
forward the port over SSH from elsewhere.

### Can I get a separate virtual host for staging/development?

If you really need one, we might be able to work something out. Email
`hostmaster@ocf` with details.

[dpkg]: https://www.debian.org/distrib/packages#search_packages
