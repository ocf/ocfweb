[[!meta title="sorry: disable an OCF account"]]

## Introduction

`sorry` is the command used to disable OCF accounts. Accounts are disabled
for various reasons, including but not limited to violating OCF/university
policies, security issues, lack of contact information, etc. Alumni also
sometimes request to have their accounts disabled to stop vhosts, take down
information, or for myriad other reasons.

## Usage/Example

    Usage: sorry [user to be sorried] [sorry file]

Sorrying a user changes their login shell to the sorryshell,
(/opt/share/utils/bin/sorried), copies the sorry file (containing the reason
they were sorried) to ~user/.sorry, `chmod 000`'s the user's httpdir, `chmod
500`'s the user's homedir, and adds the user to the "sorry" group, before
emailing them with the reason they were sorried. If a sorried user attempts to
log in, they will be rebuffed.

You will need an admin and root principal (or, atleast, ocfroot membership) in
order to run this command, which should preferably be run on supernova in order
to find all the appropriate files.

All sorry files are stored in [ocf/utils](//github.com/ocf/utils) under
`staff/acct/sorry/`, which is where they should be edited if necessary. Puppet
clones this repo to `/opt/share/utils/` on all the computers.

After sorrying a user, make sure to run the `note` command to document the
reasoning to ~staff/User_Info. This reason will be read to future users running
`check` on the sorried user.

[[Unsorrying | doc staff/scripts/unsorry]] a user is also possible.

If a user is sending too much mail, it may be easier to `nomail` the user
instead of sorrying their account. This involves adding the user to
`/etc/postfix/ocf/nomail` on anthrax, at which point their ability to send
mail will be removed.

See `how sorry` for more information on the sorry command itself.
