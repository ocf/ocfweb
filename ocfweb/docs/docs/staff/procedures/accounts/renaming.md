[[!meta title="Renaming Accounts"]]

Sometimes it's desirable to rename an OCF account.

Renaming accounts is not a well-defined procedure, and touches several
parts of the OCF's infrastructure, so it's easy to mess up. This document
serves to outline the necessary steps and provide some guidance on how a
rename might be achieved.

**This document is intended _purely_ as an overview. Do not attempt anything
contained herein without understanding what you are doing and what services
you are affecting. This document is up to date as of 02-2017.**

The steps to rename an account are roughly the following:

1. Move the homedir and webdir
2. Rename the user in Kerberos
3. Rename the user in LDAP
4. Change the user's symlinks
5. Change the user's name in the print quota system
6. Update the user's crontabs
7. Update the user's MySQL database if they have one
8. Update vhosts
9. Document the change using `note`

There are other considerations to be made if the user having their name
changed is a staff member. See the bottom of this page for more
information in that regard.


## Performing the rename

Do this on `supernova`. You'll need root and an `/admin` principal.

### Document the name change

Start by `note`ing the change before you rename the user. `note` checks
LDAP and will fail if you attempt to do it afterwards because the old
user won't exist.

    $ note -u oldname 'renaming oldname -> newname'

### Move user directories

    $ mv /home/o/ol/oldname /home/n/ne/newname

    $ mv /services/http/user/o/oldname /services/http/user/n/newname

### Rename the user in Kerberos

    $ kadmin rename oldname newname

### Rename the user's entries in LDAP

    $ kinit you/admin ldapvi uid=oldname

Edit the entries that say "uid=oldname" to "uid=newname", and change the
`homeDirectory` entry accordingly.

After renaming the user in Kerberos and LDAP, flush the name cache
by doing:

    $ nscd -i passwd

### Symlinks

The main symlink should be `public_html` in the user's homedir which
points to their webdir. You can delete it and either recreate it
manually or by running `makehttp` as the new user. Make sure the
symlinks are owned by the new user and not you or root after you're done.

    $ cd ~newname && rm public_html
    $ ln -s /services/http/users/n/newname ~newname/public_html

    $ cd ~newname && rm public_html
    $ makehttp

### Print Quota

Log into `pma.ocf.berkeley.edu` as `ocfprinting`. Run some SQL to
rename the user in the quota history. For example, you might try

    UPDATE `jobs` SET `user` = '<new>' WHERE `user` = '<old>';
    UPDATE `refunds` SET `user` = '<new>' WHERE `user` = '<old>';

### Move Crontabs

Crontabs, among other things, are located at `supernova:/services/crontabs/`
There are crontabs for three servers users might log into: supernova
for staff, tsunami for regular users, and werewolves for apphosting groups.

    $ sudo mv /services/crontabs/<server>/oldname \
              /services/crontabs/<server>/newname

### MySQL database

Renaming databases on a live system is a bad idea, in general. Be careful
when following what StackOverflow says to do. Hopefully the user doesn't even
have a database.

Depending on what data is in the user's database, there are a few options.
The easiest should be to run `makemysql` on `tsunami` as the new user, and
then delete the database of the old user.

The following commands may also work, if other options are unsuitable.

    $ mysqldump -u root -p -v oldname > old.sql
    $ mysqladmin -u root -p create newname
    $ mysql -u root -p newname < old.sql

After any data migrations have taken place, run `makemysql` on `tsunami`
anyways as the new user. It won't attempt to create a new database if one
already exists but it will still set up grants for the new user.

### Update vhosts

If the account being renamed belongs to a group, it may be necessary to
change their vhost configurations. These configurations are stored at
`supernova:~staff/vhost/`. Look through `vhost.conf`, `vhost-app.conf`
and `vhost-mail.conf`, editing the groups's entry if necessary to reflect
the new name.

### Documenting what you've done

Log the rename after it's done by using `note`.

    $ note -u newname 'renamed oldname -> newname'

That should be it. Don't attempt what's written in this document verbatim,
especially if it hasn't been updated in a while, or without being/notifying
a site manager.

### Renaming staff: additional considerations

[comment]: # (the following was suggested by daradib 2017-02-08)
Because staff members have more privileges and access to more OCF services,
further changes are necessary to completely rename a staff user compared to a
regular user. These include updating Google Apps (@ocf.berkeley.edu emails)
and the appropriate mailing lists, changing the user's entries in the OCF's
LDAP groups, updating the user's principals in kadmind.acl, changing the
user's name in RT, updating `staff_hours.yaml`, and potentially other things
as well. It is not advised for a staff member to have their account name
changed.

### Closing thoughts

In many cases, it may be better to not rename the account, and simply to
sorry it and create a new account instead. Besides being simpler, this has
the benefit of preventing the old account name from being reused, and any
links or email addresses associated with the old account will also fail rather
than redirecting, which may desirable.
