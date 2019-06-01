[[!meta title="unsorry: re-enable a sorried account"]]

## Introduction

For various reasons, we've had to disable accounts. Some for weak passwords,
some for security vulnerabilities, or myriad other reasons. If an account
is [[sorried|doc staff/howto/account-management/sorry]], once you've made sure the original problem
has been resolved (you can check `User_Info` via [[check| doc staff/howto/account-management/check]])
you can `unsorry` their account and let them log in again.

`unsorry` will remove the user from the sorry group, re-enable a login shell,
and generally allow them to use their account again. Occasionally more
than simply `unsorry` may be necessary depending on changes in the
infrastructure.

`unsorry` should be run on supernova.

## Usage/Example

    $ sudo unsorry username

It may also be necessary to run `nscd -i passwd` on **`tsunami`**.

Make sure to document all `sorry`ing and `unsorry`ing using [[note|doc staff/howto/account-management/note]]
