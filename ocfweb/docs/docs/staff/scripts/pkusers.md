[[!meta title="pkusers (modify a user's printing account)"]]



## Introduction

pkusers is a program supplied by the PyKota package that manages PyKota users. When a user prints for the first time a PyKota user is created for them. This keeps track of their quota, and how much to charge each user for a print job.

## Usage Scenarios

### Add/subtract/set pages to/from/for an account

    ~$ pkusers -b <adjustment> <username>
Add 8 pages:

    ~$ pkusers -b +8 username
Subtract 8 pages:

    ~$ pkusers -b -8 username
It is also possible to set an exact number of pages by omitting the sign:

    ~$ pkusers -b 8 username
This is **not** recommended, however, as it has the potential to wipe the page
quotas for every PyKota user.

### List detailed information about a user

    ~$ pkusers -L username
or

    ~$ pkusers --list username

### Create a new user

    ~$ pkusers -a username

### Delete a user

    ~$ pkusers -d username

### Viewing and modifying semester quotas

On [[pollution|doc staff/backend/servers]] only,

    ~$ pkusers -x /etc/pykota/pykota.semester <command>
or

    ~$ pkusers --config /etc/pykota/pykota.semester <command>
