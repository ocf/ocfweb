[[!meta title="Jenkins"]]

[Jenkins](https://jenkins.ocf.berkeley.edu/) is the tool we use for continuous
integration and continuous delivery (TM) at OCF. All that means is that when
you push code,

* Jenkins will test that code,
* Jenkins will build that code (if applicable),
* and then Jenkins will deploy that code.

Ideally all projects at OCF will go through this pipeline of being tested
before deployed, though currently some don't (or some only use some portion,
such as deploying without any tests).


## Making changes to Jenkins

Anyone in group `ocfroot` can log in to Jenkins (using their OCF username and
password) and will have full access to Jenkins.

Sadly, while the installation of Jenkins is controlled via Puppet, its
configuration is not. Configuring by Puppet would be nice, but it would mean
changes would need to be made inside Puppet instead of the web UI.

In practice it seems most people in industry are still using the web UI for
configuration anyway.


## Jenkins security model

There are three users configured on the Jenkins server (`reaper`):

* `jenkins`, the user created by the Debian package. It is used for running the
  Jenkins master but not for performing any work.

* `jenkins-slave`, a user we create. It is used for running build jobs with
  potentially untrusted code. **However,** it's not secure enough to run
  totally untrusted code, since all jobs run under this user.

* `jenkins-deploy`, a user we create. It is used for running build jobs tagged
  `deploy`, whose only purpose is intended to be *deploying* code which has
  been built or tested in a previous step. The user has a Kerberos keytab for
  the `ocfdeploy` user and our PyPI key in its home directory. Jobs such as
  `upload-deb` or `puppet-trigger` fall under this user.

Within Jenkins, we configure two "slaves" which are really on the same server,
but execute by launching the `slave.jar` file as the `jenkins-slave` or
`jenkins-deploy` user (via passwordless sudo from the `jenkins` user,
effectively dropping permissions).

The jobs are configured to run on either `jenkins-slave` (the default) or
`jenkins-deploy` (for deploy jobs).

This is a bit complicated, but it allows us both better security (we no longer
have to worry that anybody who can get some code built can become ocfdeploy,
which is a privileged user account) and protects Jenkins somewhat against bad
jobs that might e.g. delete files or crash processes.

Of course, in many cases once code builds successfully, we ship it off
somewhere where it gets effectively run as root anyway. But this feels a little
safer.
