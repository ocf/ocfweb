[[!meta title="unsorry: re-enable a sorried account"]]

## Introduction

`unsorry` is the inverse of [`sorry`](//ocf.io/docs/staff/scripts/sorry/).
It will remove the user from the sorry group, re-enable a login shell,
and generally allow them to use their account again. Occasionally more
than simply `unsorry` may be necessary depending on changes in the
infrastructure.

`unsorry` should be run on supernova.

## Usage/Example

    $ unsorry username

Make sure to document all `sorry`ing and `unsorry`ing using [`note`](//ocf.io/docs/staff/scripts/note/).
