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


## Making changes to Jenkins    {making-changes}

Anyone in group `ocfroot` can log in to Jenkins (using their OCF username and
password) and will have full access to Jenkins.

Sadly, while the installation of Jenkins is controlled via Puppet, its
configuration is not. Configuring by Puppet would be nice, but it would mean
changes would need to be made inside Puppet instead of the web UI.

In practice it seems most people in industry are still using the web UI for
configuration anyway.


## Jenkins security model    {security}

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


## Jenkins for GitHub projects    {github}

### On the master branch

To test GitHub projects when you push to master:

1. Configure the "GitHub Project" URL to point to the main page of the project
   (for example, https://github.com/ocf/puppet/).

2. Under "Source Code Management", select "Git" and add the repository URL (for
   example, https://github.com/ocf/puppet/).

3. Under "Build Triggers", check "Build when a change is pushed to GitHub".

4. On GitHub, go to "Settings" then "Webhooks & services". Add a new "Jenkins
   (GitHub Plugin)" service with URL
   `https://jenkins.ocf.berkeley.edu/github-webhook/`.

You can create additional steps or organize pipelines if desired (for example,
if you'd like to first test and then deploy).


#### Adding a "Build Status" badge to the README

You might like to add a fancy "Build Status" badge to the README. From the
project page, choose the "Embeddable Build Status" icon, then choose "Markdown
(with view), unprotected". You can optionally change the link to point to the
pipeline view rather ther than just the individual job.


### Building and tagging pull requests

Jenkins can build and tag pull requests with their build status, similar to
Travis. To configure this for a repository, create a new job specifically for
testing pull requests. For example, `puppet-test-pr`.

1. Configure the "GitHub Project" URL to point to the main page of the project
   (for example, https://github.com/ocf/puppet/).

2. Under "Source Code Management", select "Git" and add the repository URL (for
   example, https://github.com/ocf/puppet/).

3. Under "Source Code Management", change "Branch Specifier" to `${sha1}`.

4. Also under "Source Code Management", change "Refspec" (it's under Advanced)
   to `+refs/pull/*:refs/remotes/origin/pr/*`.

5. Under "Build Triggers", check "GitHub Pull Request Builder", and then check
   "Use github hooks for build triggering".

6. Under "GitHub Pull Request Builder", delete all lines under "Admin List" (if
   there are any). Add "ocf" as the only line to the "List of organizations"
   box.

7. On GitHub, under "Settings" and "Webhooks & services", add a new webhook
   with payload URL `https://jenkins.ocf.berkeley.edu/ghprbhook/`, content type
   `application/json`, and the secret (it's in `supernova:/opt/passwords`).
   Choose to trigger only on certain events:

   * Commit comment
   * Issue comment
   * Issues
   * Pull Request
   * Pull Request view comment

   (These might not all be necessary, but I don't know the exact list.)

8. On GitHub, add the "Bots" group admin access to the repository. This is
   necessary so that it can set commit statuses.
