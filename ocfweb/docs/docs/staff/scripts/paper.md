[[!meta title="paper: view and modify print quotas"]]

## Introduction

The `paper` script is used to list and modify user print quotas. When users
print documents, their print quota is updated in a central database on `mysql`
that is also checked to make sure users have enough print quota before sending
their document(s) to the printer. This database can be queried and modified by
the `paper` script, which internally uses `ocflib` to access the database.

The `paper` script can be used from anywhere to list pages remaining per day
and per semester, but can currently only be used to change print quotas by
issuing refunds from `supernova`.

## Usage Scenarios

### View help (shows possible commands and arguments)

    $ paper -h
    $ paper view -h
    $ paper refund -h

### View balances

For yourself:

    $ paper

For other users:

    $ paper view <user>


### Issue refunds (change user balances)

Refunds can be positive or negative, so you can add or subtract quotas using
this method. By default they are positive, so you are refunding them for pages
wrongly used. Make sure to surround the reason in quotes if it contains spaces,
otherwise the command will not work.

    $ paper refund --pages <num_pages> --reason "<reason>" <user>
