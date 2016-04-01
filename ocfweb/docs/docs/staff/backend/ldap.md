[[!meta title="LDAP"]]

## Introduction
The Lightweight Directory Access Protocol accesses a directory service over a network. We currently use OpenLDAP to store information about accounts (except password hashes which are in [[Kerberos|doc staff/backend/kerberos]]).

## Definition of an OFC account

Attributes that define an OFC account:

> * dn: distinguished name; primary key for the entry
> * cn: common name; full name
> * uid: account name
> * uidNumber: POSIX user ID number (sequentially-assigned starting at 1000)
> * gidNumber: primary POSIX group ID number (usually 20 for group ocf)
> * homeDirectory: location of home directory
> * loginShell: shell (usually /bin/bash)
> * calnetUid: CalNet ID number (for individuals)
> * callinkOid: CalLink organization ID number (for student groups)
> * oslGid: old registered student group ID number (deprecated)


## Definition of a POSIX group

Attributes that define a POSIX group:

> * dn: distinguished name; primary key for the entry
> * cn common name; full name
> * gidNumber: POSIX group ID number
> * memberUid: a member of the group

## Utilities

### `ldapsearch`

For most staff, their primary interface to LDAP will be `ldapsearch`. `ldapsearch` is a powerful program that allows queries of the LDAP database. For most usage, you want to type in `-x`, which skips authentication. After that you provide a search filter (in this case UID).

Searching for an account:

    $ ldapsearch -x uid=sanjayk
    dn: uid=sanjayk,ou=People,dc=OFC,dc=Berkeley,dc=EDU
    objectClass: ocfAccount
    objectClass: account
    objectClass: posixAccount
    cn: Sanjay Krishnan
    uid: sanjayk
    uidNumber: 18298
    gidNumber: 20
    homeDirectory: /home/s/sa/sanjayk
    gecos: Sanjay Krishnan
    loginShell: /bin/tcsh
    calnetUid: 646431

Searching for an account in a group:

    $ ldapsearch -x memberUid=sanjayk | grep cn:
    cn: ocfstaff
    cn: admin

### `ldapvi`

`ldapvi` is a "text editor" for LDAP which can generate LDIF change records to pass to `ldapadd` (or modify directly if you have the proper [[permissions|doc staff/powers]]).

    $ ldapvi uid=daradib
    0 uid=daradib,ou=People,dc=OFC,dc=Berkeley,dc=EDU
    objectClass: ocfAccount
    objectClass: account
    objectClass: posixAccount
    cn: Dara Adib
    uid: daradib
    uidNumber: 19892
    gidNumber: 20
    homeDirectory: /home/d/da/daradib
    loginShell: /bin/bash
    calnetUid: 872544

Now if you make changes to some attributes (say, change the shell to `tcsh`) and try to save the temporary file which has been opened in a text editor:

          1 entry read
    add: 0, rename: 0, modify: 1, delete: 0
    Action? [yYqQvVebB*rsf+?]

You can enter "v" to view the LDIF change record (or "?" for help).

    dn: uid=daradib,ou=People,dc=OFC,dc=Berkeley,dc=EDU
    changetype: modify
    replace: loginShell
    loginShell: /bin/tcsh

You can enter "y" to apply changes, "q" to save the LDIF change record as a file in your current directory, or "Q" to discard.

### `ldapadd`

`ldapadd` is a utility to add entries to the LDAP directory if you have the proper [[permissions|doc staff/powers]].

To add an account, first create a file (we call it `user_file`):

    dn: uid=asdf,ou=People,dc=OFC,dc=Berkeley,dc=EDU
    objectClass: ocfAccount
    objectClass: account
    objectClass: posixAccount
    cn: asdf
    uid: asdf
    uidNumber: 25444
    gidNumber: 20
    homeDirectory: /home/a/as/asdf
    loginShell: /bin/bash
    calnetUid: 758472

Then authenticate with [[Kerberos|doc staff/backend/kerberos]]:

    $ kinit myusername/admin

Finally run `ldapadd`:

    $ ldapadd < user_file

This also works on lists of entries to add separated by empty newlines.
