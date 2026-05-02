ocfweb
==========
[![Build Status](https://jenkins.ocf.berkeley.edu/buildStatus/icon?job=ocf/ocfweb/master)](https://jenkins.ocf.berkeley.edu/job/ocf/job/ocfweb/job/master)
[![Code Health](https://landscape.io/github/ocf/ocfweb/master/landscape.svg?style=flat)](https://landscape.io/github/ocf/ocfweb/master)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

[The main ocf website.](https://www.ocf.berkeley.edu/)


## Working on `ocfweb` on the ocfstaff remote dev server

1. Open a terminal on your local host and run `ssh koi.ocf.io`.
2. Then, run `git clone git@github.com:ocf/ocfweb.git`, `cd ocfweb`, then `devenv up`.
    - It may take about several minutes for all of the dependencies to install the first time. Give it at least 10 min.
    - You will see a process-compose tui appear, with a process called "web" and the logs visible. Your user's port is what is generated in the log line `Running on https://koi.ocf.berkeley.edu:YOUROWNPORT`, based on your uid. This is to avoid conflicts with other users who might also be running dev servers on koi.
3. Open an SSH tunnel on your local host (**not** on `koi` or other OCF servers): `ssh -L YOUROWNPORT:localhost:YOUROWNPORT koi`
    - to avoid this extra step in the future, add the following to your `~/.ssh/config`:
    ```
    Host koi
        HostName koi.ocf.berkeley.edu
        LocalForward YOUROWNPORT localhost:YOUROWNPORT
    ```
4. Go to https://localhost:YOUROWNPORT in your local browser!


## BELOW THIS IS OUTDATED. WIP

---

We recommend following all of these steps
[on supernova](https://www.ocf.berkeley.edu/docs/staff/procedures/ssh-supernova/),
the staff login server, because it is already configured to run ocfweb in
development mode with minimal extra setup.

Clone the repo, and be sure to check out submodules:

    $ git submodule update --init
    $ make install-hooks

If you get an error about not being able to import bootstrap, it's because you
forgot to run the second command.

### Running in development mode

On supernova<sup>[0]</sup>run `make dev`. The first time will take a while, but
future runs will be almost instant thanks to
[pip-faster](https://github.com/Yelp/pip-faster).

It will start listening on a deterministically random port (really, 8000 plus
the last 3 digits of your user id) which is printed to you. You can then view
the site in development.


### Building SCSS

Run `make scss` to build SCSS. You can also use `make watch-scss` to rebuild it
automatically when SCSS files change.


### Running tests

To run tests locally, run `make test`. Please don't push to master with
failing tests—Jenkins will refuse to deploy your code, and nobody will be able
to deploy until it's fixed.

If you make a pull request to the OCF GitHub organization from your fork of
ocfweb, Jenkins will attempt to build and test your branch automatically.
If your build fails, you can log into Jenkins to see which tests you've failed
and fix them, if running `make test` locally didn't already tell you.

You can run individual tests with `venv/bin/pytest -k <test_name>` or
`venv/bin/pytest <test_file>::<test_name>` if running all tests is too slow.


### Running pre-commit

We use [pre-commit](https://pre-commit.com/) to lint our code before commiting.
While some of the rules might seem a little arbitrary, it helps keep the style
consistent, and ensure annoying things like trailing whitespace don't creep in.

You can simply run `make install-hooks` to install the necessary git hooks;
once installed, pre-commit will run every time you commit.

Alternatively, if you'd rather not install any hooks, you can simply use `make
test` as usual, which will also run the hooks.

Almost all build failures of ocfweb can be tied to something `pre-commit`
probably would have caught.


### Installing packages

To install a package to the production environment, add it to
`requirements-minimal.txt`, then run `make update-requirements`. Similarly, to
install to the development environment, add to `requirements-dev-minimal.txt`
and run `make update-requirements`. Use as loose a version requirement as
possible, e.g. try `django` or `django>=1.10,<1.10.999` before
`django==1.10.0`.


-----

[0]: If you have a staff VM, you can also use that to run ocfweb. You will have
to add the `ocf_ocfweb::dev_config` class to your
[Hiera node config](https://github.com/ocf/puppet/tree/master/hieradata/nodes).
Specifically, add:

    classes:
        - ocf_ocfweb::dev_config

It's probably easier to just run everything on `supernova`.
