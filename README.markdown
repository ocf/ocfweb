atool
====

## About

atool is a Django-based web application for OCF users.

### Features

* Request new individual accounts
* Reset account passwords (via CalNet login)
* Run commands from the web (like `paper` or `makehttp`)
* Request virtual hosting

### What goes here

In general, [ocflib](https://github.com/ocf/ocflib) should be where all
reusable logic (i.e. things that are not Django or web-specific) goes. This
helps us to reuse the same code for the web app as our command-line tools.

Ideally, this application consists of the tiny amount of code needed to deal
with authentication/forms/web things, and the bulk of the account logic resides
in ocflib.

## Requirements

atool is targeted for Python versions 3.2 and 3.4. Install requirements via
`pip3 install -r requirements.txt`.

Generally, the latest version of [ocflib](https://github.com/ocf/ocflib) is
expected.

## Development

You can use the `dev-accounts` server to test changes. To run the app in
development mode, use `make dev`.

To lint before pushing, use `make check`.

## Deploying

Puppet checks out the latest master from GitHub, and will auto-deploy when it
changes. Simply pushing to master is enough, though it will take up to 30
minutes for Puppet to run and deploy your changes.

If for some reason you want to restart the server manually, you can use
daemontools commands like `svc -h /etc/service/atool`.
