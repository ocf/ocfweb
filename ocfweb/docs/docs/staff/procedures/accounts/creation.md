[[!meta title="Account Creation"]]
# Creating Accounts

This page was entirely out-of-date, so the old content was removed. Some
context for now until it gets updated:

    [14:57:20] <ckuehl> the terms are confusing
    [14:57:35] <ckuehl> atool = django webapp frontend for approve, chpass, some other things
    [14:57:49] <ckuehl> create = command-line tools for actually *creating* the accounts which have been queued by atool or approve
    [14:57:59] <ckuehl> approve = staff cli for queueing group accoutns for creation by create
    [14:58:22] <ckuehl> filter = lightweight script that calls create with appropriate environment variables to let staff manually filter accounts
    [14:58:33] <ckuehl> so atool = accounts.ocf.berkeley.edu

In the mean time, if you want to filter accounts which are pending admin
approval, run `filter` (requires root) on supernova.

# Updating create

If you have patched create, make sure to push your changes to
[GitHub](https://github.com/ocf/create) and deploy on OCF systems with the
command:

        $ cd /opt/ocf/packages/create && sudo git pull
