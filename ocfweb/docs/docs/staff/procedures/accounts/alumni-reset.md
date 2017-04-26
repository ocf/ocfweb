[[!meta title="Alumni Account Reset"]]

Occasionally former OCF members want to re-enable their accounts after
they've been disabled for various reasons, including weak passwords,
lack of CalNet UID, lack of Kerberos principal, etc.

These are the relevant steps to take in various situations.

#### Missing CalNet UID    {calnet}

If an alumni cannot use the online password reset function to reset the
password on their account, but they do have a CalNet login, you can manually
add the Calnet UID to their account in LDAP to let them perform a password
reset. They may also need to have a Kerberos principal added for them.

Please make sure to confirm the user's CalNet ID using the Berkeley Directory.

To perform the association, simply follow the steps outlined in the
[[LDAP Association|doc staff/procedures/accounts/association]] documentation
with regards to adding the `calnetUid` record.

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

    $ kadmin add <username>

You will need an admin principal yourself to do this. Choose the default options
when kadmin presents them.

#### Disabled Account

For various reasons, we've had to disable alumni accounts in the past. Some for weak
passwords, some for security vulnerabilities, or myriad other reasons. If an account
is [[sorried|doc staff/scripts/sorry]], once you've made sure the original problem
has been resolved (you can check `User_Info` via [[check| doc staff/scripts/check]]
you can [[unsorry|doc staff/scripts/unsorry]] their account and let them log in
again. It may also be necessary to run `nscd -i groups` on **`tsunami`**, as well as
`chown -R <username>:ocf ~<username>` to let them log in and access their files.
Make sure to [[note| doc staff/scripts/note]] your changes as necessary.


#### Manual Verification of Alumni Identity

Before re-enabling access to an alumni's account, one should verify their identity.
If they do not have a CalNet UID or are otherwise lacking a reasonable method of
verifying their identity, it may be necessary to request manual verification of
identity. Pursuant to the [[instructions for alumni| doc services/account]], if
you receive a reactivation request from an alum and need to manually verify their
identity, direct them to send you the required documentation at a private address
and destroy the documentation as soon as possible.
