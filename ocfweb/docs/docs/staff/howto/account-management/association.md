[[!meta title="LDAP association"]]

New individual accounts have a `calnetUid` attribute in
[[LDAP|doc staff/backend/ldap]] which is used for
[[changing passwords online|change_password]], querying CalNet when running
[[`check`|doc staff/howto/account-management/check]], and producing aggregate counts of
the number of members by university affiliation.

Similarly, group accounts have a `callinkOid` attribute.

Old accounts, especially if previously disabled, may be missing the
`calnetUID` or `callinkOid` attribute. Please add it when enabling accounts.
If unknown or a group other than a registered student organization, set it
to `0`. The `0` is still useful for distinguishing between individuals and
groups based on the attribute name.

Occasionally, it is useful to allow someone to reset a group account password
online when they are not a signatory, namely when the account is not for a
registered student organization. This is done by associating the user's CalNet
ID with the account record in LDAP.

Open the LDAP record for editing.

    $ kinit <staffusername>/admin ldapvi uid=<username>

After looking up the user's UID in the [University
directory](http://www.berkeley.edu/directory), add it to the record with a line
like this:

    calnetUid: 6081

If the `mail` attribute is missing, but you know of a contact email address for
the account, please add it as well.

Save the file to update LDAP. Now, the user can
[[change the account password online|change_password]].

CalNet association is only meant to be temporary and must be reverted once the
password has been reset by removing this line. It can cause problems with
individual/group acount detection in scripts if an account has both
`callinkOid` and `calnetUid` fields. If an account is associated in an RT
ticket, leave the ticket open until the password has been reset and the account
disassociated.
