atool
====
[![Build Status](https://travis-ci.org/ocf/atool.svg)](https://travis-ci.org/ocf/atool)

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

To deploy, push to master on GitHub, then trigger a puppet run on the
`accounts` server. Run `svc -h /etc/service/atool` to restart the Gunicorn
server.
