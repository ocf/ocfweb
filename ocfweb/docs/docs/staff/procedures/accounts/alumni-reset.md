[[!meta title="Alumni account reset"]]

Occasionally former OCF members want to re-enable their accounts after
they've been disabled for various reasons, including weak passwords,
lack of CalNet UID, lack of Kerberos principal, etc.

These are the relevant steps to take in various situations.

#### Missing CalNet UID    {calnet}

If an alumni cannot use the online password reset function to reset the
password on their account, but they do have a CalNet login, you can manually
add the Calnet UID to their account in LDAP to let them perform a password
reset. They may also need to have a Kerberos principal added for them.

Please make sure to confirm the user's CalNet ID using the Berkeley Directory,
or by searching the Cal Alumni Network. Alumni profile URLs are in the form
`https://cal.berkeley.edu/profile.php?u=<calnet_uid>`. You may need an
actual alumnus to perform the search for you, if you are so inclined but
unable to access the page on account of your youth.

To perform the association, simply follow the steps outlined in the
[[LDAP Association|doc staff/procedures/accounts/association]] documentation
with regards to adding the `calnetUid` record. However, don't delete it after
you're done.

#### Missing Kerberos principal    {kerberos}

In 2011, we transitioned our password database to Kerberos. Anyone who
logged into their OCF account during the transition had their credentials
migrated, but alumni who didn't log in may be missing a
[[Kerberos principal|doc staff/backend/kerberos]]. For them, it is necessary
to manually add one.

This error manifests itself as the following when a user attempts to reset
their password:

    kadmin Error: kadmin: cpw <username>: Principal does not exist

To add the principal, run the following:

    $ kadmin add --use-defaults --random-password <username>

You will need an admin principal yourself to do this. `kadmin` will return the
password and you can relay this to the alumni.

#### Disabled Account    {sorried}

If the account is [[sorried|doc staff/scripts/sorry]], refer to the documentation
for [[unsorry|doc staff/scripts/unsorry]] to re-enable the account.

#### Manual Verification of Alumni Identity    {verify}

Before re-enabling access to an alumni's account, one should verify their identity.
If they do not have a CalNet UID or are otherwise lacking a reasonable method of
verifying their identity, it may be necessary to request manual verification of
identity. Pursuant to the [[instructions for alumni| doc services/account]], if
you receive a reactivation request from an alum and need to manually verify their
identity, direct them to send you the required documentation at a private address
and destroy the documentation as soon as possible.
