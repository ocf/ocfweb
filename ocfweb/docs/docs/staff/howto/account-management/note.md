[[!meta title="note: add notes to a user account"]]

## Introduction

`note` adds notes to the user's entry in `~staff/User_Info`. It is used to log
important information about a user, for example, if they've been sorried
(and why), if their password was reset, if some admistrative action has been
performed on their account, e.g. renaming the account, or for myriad other
reasons where some documentation should be made about an OCF account.

`note` should be run on supernova.

## Usage/Example

    $ note -u username [note]

`note` will append the note-taking user's username, the day's date, the noted
user's username, and the note to `~staff/User_Info`, where it can later be retrieved by
[[`check`|doc staff/howto/account-management/check]].
