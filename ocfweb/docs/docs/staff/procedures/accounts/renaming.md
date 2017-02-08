[[!meta title="Renaming Accounts"]]

Sometimes OCF accounts need to be renamed. Users sometimes make mistakes
when creating their accounts, or group accounts might need to be changed,
or for several other reasons.

Renaming accounts touches several parts of the OCF's infrastructure, and
as parts are changed, this document may go out of date, but renaming an
account is an informative way to learn about how some parts of the OCF work.

The steps to rename an account are roughly the following:
1. Move the homedir and webdir
2. Rename the user in Kerberos
3. Rename the user in LDAP
4. Change the user's symlinks
5. Change the user's name in the print quota system
6. Update the user's crontabs
7. Update the user's MySQL database if they have one
8. Document the change using `note`

## Performing the rename

Do this on supernova. You'll need root and an /admin principal.

### Move user directories

    $ mv /home/<old[0]>/<old[:1]>/<old> /home/<new[0]>/<new[:1]>/<new>
    $ mv /services/http/user/<old[0]>/<old> /services/http/user/<new[0]>/<new>

### Rename the user in Kerberos

    $ kinit <you>/admin kadmin rename <old> <new>

### Rename the user's entries in LDAP

Open the LDAP record for editing

    $ kinit myusername/admin ldapvi uid=<old>

Edit the entries that say "uid=<old>" to "uid=<new>", and change the
homeDirectory entry accordingly, before saving and exiting.

After renaming the user in Kerberos and LDAP, flush the name cache
by doing

    $ nscd -i passwd

### Symlinks

The main symlink should be `public_html` in the user's homedir which
points to their webdir. You can delete it and either recreate it
manually or run `makehttp`.

    $ cd ~<new> && rm public_html
    $ ln -s /services/http/users/<new[0]>/<new> ~<new>/public_html

    $ cd ~<new> && rm public_html
    $ makehttp

### Print Quota

Go to pma.ocf.berkeley.edu and log in as ocfprinting. Run some SQL to
rename the user in the quota history. For example, you might try

    UPDATE `jobs` SET `user` = '<new>' WHERE `user` = '<old>';
    UPDATE `refunds` SET `user` = '<new>' WHERE `user` = '<old>';

### Move crontabs

Crontabs, among other things, are located at supernova:/services/
There are crontabs for three servers users might log into: supernova
for staff, tsunami for regular users, and werewolves for apphosting
groups.

    $ sudo mv /services/crontabs/<server>/<old> \
              /services/crontabs/<server>/<new>

### MySQL database

Renaming databases on a live system is a bad idea, in general. Use your sense
when
following what StackOverflow says to do. Hopefully the user doesn't even have
a database.

Depending on what data is in the user's database, it might be simpler to use
PMA to
rename the database, or if not,

    $ mysqldump -u root -p -v <old> > <old>.sql
    $ mysqladmin -u root -p create <new>
    $ mysql -u root -p <new> < <old>.sql

Then grant the new user the appropriate permissions on the newly renamed
database.

### Documenting what you've done

Log the rename after it's done by using `note`.

That should be it.
