[[!meta title="CalNet Association"]]
# Associate an account with a CalNet ID

Occasionally, it is useful to allow someone to reset a group account password
online when they are not a signatory, namely when the account is not for a
registered student organization. This is done by associating the user's CalNet
ID with the account record in LDAP.

Open the LDAP record for editing.

    $ kinit myusername/admin ldapvi uid=groupname

After looking up the user's UID in the [University
directory](http://www.berkeley.edu/directory), add it to the record with a line
like this:

    calnetUid: 123456

Save the file to update LDAP. Now, the user can update the account password at
the usual URL: [https://accounts.ocf.berkeley.edu/change-password](https://accounts.ocf.berkeley.edu/change-password)

CalNet association is only meant to be temporary and must be reverted once the
password has been reset by removing this line. It can cause problems with
individual/group acount detection in scripts if an account has both
<code>callinkOid</code> and <code>calnetUid</code> fields. If an account is
associated in an RT ticket, leave the ticket open until the password has been
reset and the account disassociated.
