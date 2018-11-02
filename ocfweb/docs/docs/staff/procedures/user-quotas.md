[[!meta title="User disk quotas"]]

We use the standard Unix quota utilities to set disk quotas.


### Summary of useful commands

All of these can be executed on `filehost`. Some of them also work on other
servers which mount NFS.


#### View your own quota

    quota


#### View another user's quota

    quota -u daradib


#### Print a summary of every user's disk quota

    repquota /dev/mapper/vg-homes


#### Setting custom disk quotas

Sometimes we want to set a custom disk quota for a staff member or other
special snowflake (e.g. perhaps a user wants to host their research or
something on OCF, which we encourage).

To make an exception, just change their quota individually using `edquota -u
{username}`. This will open a file in your editor showing their quota. Change
the `soft` and `hard` columns to the number of kibibytes you wish to allocate,
then save the file.

You can disable the quota entirely by setting `0` for both the `soft` and
`hard` limit, but this is **not recommended** because the next time somebody
tries to raise disk quotas, it will "raise" your quota from "no quota" to the
new quota. To mimic an infinite quota, just give the account a very large quota
instead.


## Raising disk quotas for every user

Are you trying to raise disk quotas for every user? Congratulations on finding
this page! The SM who wrote this section spent a couple of hours trying to
figure out *how in the hell* our automatic disk quotas were working, despite
all internet documentation claiming there is no way to set default disk quotas.

Indeed, you cannot configure a default quota. You can, however, set quotas for
non-existent users! We've set quotas for user IDs 1000 through 99999 in order
to mimic default users.

To raise disk quotas, you can use a command like:

```bash
soft_limit="5242880"  # 5 GiB in KiB
hard_limit="5767168"  # 5.5 GiB in KiB

for i in $(seq 1000 99999); do
    quotatool -b -Rr  -q "$soft_limit" -l "$hard_limit" -u ":$i" /dev/mapper/vg-homes
done
```

The flags assure that we set a block limit (rather than an inode limit) and
that we only raise quotas (so that we don't accidentally lower the quota of a
special snowflake).

The "soft limit" is like a warning limit; it can be configured to be enforced
after a grace period, but we don't do this. In practice, we announce the limit
to the public as "X GB", with a soft limit of "X GB" and a hard limit of "X+0.5
GB".

Since the soft limit is never enforced, the real limit is the hard limit.
