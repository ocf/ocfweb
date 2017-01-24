[[!meta title="sorry: ban/disable an OCF account"]]

## Introduction

`sorry` is the command used to ban or disable OCF accounts. Accounts are banned for various reasons (users/groups being disruptive or otherwise violating OCF/university policies, security issues, lack of contact information, etc.) and alumni sometimes request to have their accounts disabled to stop vhosts, take down information, or for myriad other reasons.

## Usage/Example

    Usage: sorry [user to be sorried] [sorry file]

Sorrying a user changes their login shell to the sorryshell, (/opt/share/utils/bin/sorried), copies the sorry file (containing the reason they were sorried) to ~user/.sorry, `chmod 000`'s the user's httpdir, `chmod 500`'s the user's homedir, and adds the user to the "sorry" group, before emailing them with the reason they were sorried. If a sorried user attempts to log in, they will be rebuffed.

After sorrying a user, make sure to run the `note` command to document the reasoning to ~staff/User_Info. This reason will be read to future users running `check` on the sorried user. 

Unsorrying a user is also possible.

See `how sorry` for more information on the sorry command itself.
