[[!meta title="ssh-list: run command via SSH on many hosts simultaneously"]]

`ssh-list` is a small wrapper around `parallel-ssh` which reads lists of hosts
from LDAP.

The usage of `ssh-list` looks like:

    ssh-list <TYPE> [arguments to parallel-ssh]

The argument `<TYPE>` is interpreted by `ssh-list`, and the arguments after are
passed verbatim to `parallel-ssh`.

In most cases, you want at least `-i` in the arguments to parallel-ssh. `-i`
prints out the stdout and stderr for each host you are running the command on.
For example:

    ssh-list all -i whoami

In most cases, it's most useful to use a type like `desktop` rather than `all`.

If you get a ton of authentication errors, don't provide your password, just do
`kinit $USER` first (your Kerberos ticket probably expired, or you probably
logged in with an SSH key).

Some useful commands are below (please add more!):

### Run puppet once

Anyone in `ocfroot` can call `sudo puppet-trigger` without providing a
password.

    ssh-list desktop -i 'sudo puppet-trigger'

### Restart unused desktops

Anyone in `ocfroot` can call `sudo shutdown` without providing a password.

    ssh-list desktop -i '[ $(who | wc -l) -eq 0 ] && sudo shutdown -r now'

### Run `apt-get update` to clear apt caches

`ocfroot` can't run passwordless `apt-get`, so you need to use the `apt-dater`
keytab.

From supernova:

    sudo kinit -k -t /root/apt-dater.keytab 'apt-dater@OCF.BERKELEY.EDU' \
        ssh-list desktop -l apt-dater -i 'sudo apt-get update'
