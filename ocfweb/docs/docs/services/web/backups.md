[[!meta title="Backups/Archiving"]]

Keeping backups on hand is crucial to maintaining any website. While your data
is protected from hardware failure by the OCF's backup infrastructure, you will
find you need a backup history of your own when you need to:

* Migrate to an upgraded website
* Archive an old website with historical data
* Regress to a previous state due to a bug
* Recover from a security breach

You can make easy-to-restore backups over [[SSH|doc services/shell]] by following
the examples on this page. You could alternatively use SFTP, but this wouldn't
allow you to back up a database.


## Backing up a web directory

Making a backup of your website document tree (where all the `.html`, `.php`,
etc. files are) is as simple as making a copy of your files into your home
folder. If you maintain multiple websites, you can make individual backups of
each; otherwise, you can just back up `public_html`.

To save on storage space, you should archive and compress these backups as
either `.zip` or `.tar.gz` files. If you have a folder `~/backups` created, you
can save your website `~/public_html/website` there with the following command:

    tar czhf ~/backups/backup.tar.gz -C ~/public_html website

To restore the backup, you would first remove the contents of
`~/public_html/website` (i.e. `rm -r ~/public_html/website`) and then extract
the compressed file by changing `tar c` to `tar x`:

    tar xzhf ~/backups/backup.tar.gz -C ~/public_html website

### WARNING

Do not try to backup your `public_html` folder by copying it directly! It is
not a real directory, but a link to where the files are actually stored.
Instead, explicitly copy all the files inside to another directory or use the
the commands on this page which were written to do so.


## Backing up a database

For many websites and frameworks, the web document tree only makes up half the
site; the rest of the data resides in the database. Particularly, if you are
using WordPress, Joomla, or Drupal, you will have to backup your database
alongside your web directory.

### MySQL

If you are using a MySQL database, you can use `mysqldump` to make snapshots.
Instructions are on the [[MySQL|doc services/mysql]] page, but the basic syntax
to make a backup is

    mysqldump username > ~/backup.sql

and, to restore, is

    mysql -D username < ~/backup.sql

You should compress these files with `gzip` as they can be quite large. The
above commands can be modified to do this. To save,

    mysqldump username | gzip -c > ~/backup.sql.gz

and, to restore,

    gzip -dc ~/backup.sql.gz | mysql -D username

#### Using .my.cnf

By default, you have to enter your MySQL every time you make a backup, which is
inconvenient. Worse, if you forget the password and uses `makemysql` to reset
it, it will break your old website backups! If you want to save the trouble,
[[follow our instructions|doc services/mysql]] to create `~/.my.cnf` which will
allow you to use MySQL without entering the password by hand.


## Taking down a site

If you have an old website you want to archive and remove from public view, you
can make a backup of it using the above instructions and then delete your
webiste files and database. When deleting files, be sure to delete the contents
inside of `public_html` and not just `public_html` itself, which is a mere link.

The easiest way to remove the contents of your database is to log into
phpMyAdmin at [https://pma.ocf.berkeley.edu](https://pma.ocf.berkeley.edu)
with your OCF username and MySQL password. There, you can select all tables
using the check boxes and select `Drop` to delete them all.

If you instead wanted to delete the whole database, you could use the command

    mysqladmin -uusername -pmysql_password drop username

However, you would need to run `makemysql` to create a new database, which
would permanently change your password.


## Example backup

Suppose your OCF account name is `johndoe` and you have WordPress installed
directly in `~/public_html`. A typical backup might look like this:

    johndoe@tsunami:~$ mysqldump johndoe | gzip -c > ~/mysql-backup-7-26-15.sql.gz
    Enter password:
    johndoe@tsunami:~$ tar czhf ~/site-backup-7-26-15.tar.gz -C ~/ public_html

while a restore would look like this:

    johndoe@tsunami:~$ gzip -dc ~/mysql-backup-7-26-15.sql.gz | mysql -D johndoe
    Enter password:
    johndoe@tsunami:~$ tar xzhf ~/site-backup-7-26-15.tar.gz -C ~/ public_html

If you were using `.my.cnf`, you wouldn't even have to enter your database password.


## Security

The only real security concern is that you don't leave any backup files in your
`public_html` directory. Doing so would allow anybody to download all your raw
data and e.g. steal your website login information and find and exploit other
security vulnerabilities.
