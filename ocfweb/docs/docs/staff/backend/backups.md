[[!meta title="Backups"]]
## Backup Storage

We currently store our on-site backups across a couple drives on `hal`:

* `hal:/opt/backups` (6 TiB usable; 2x 6-TiB Seagate drives in RAID 1 in an LVM
  volume group)

  This volume group provides `/dev/vg-backups/backups-live` which contains
  recent daily, weekly, and monthly backups, and
  `/dev/vg-backups/backups-scratch`, which is scratch space for holding
  compressed and encrypted backups which we then upload to off-site storage.

## Off-Site Backups

Our main off-site backup location is [Box][box]. Students automatically get an
"unlimited" plan, so it provides a nice and free location to store encrypted
backups. We currently have a weekly cronjob that [makes an encrypted
backup][create-encrypted-backup] using GPG keys and then [uploads it to
Box.com][upload-to-box]. This takes about 20 hours combined to make and upload,
and will probably take even longer in the future as backups grow. An email is
sent out once the backup files are uploaded, and the link provided is shared
with only OCF officers to make sure the backups are kept as secure as possible,
since they contain all of the OCF's important data.  The backups are already
encrypted, but it doesn't hurt to add a little extra security to that.

### Retention

Off-site backups older than six months (180 days) are permanently deleted.

## Restoring Backups

The easiest way to restore from a backup is to look at how it is made and
reverse it. If it is a directory specified in rsnapshot, then likely all that
needs to be done is to take that directory from the backup and put it onto the
server to restore onto. Some backups, such as mysql, ldap, and kerberos are
more complicated, and need to be restored using `mysqlimport` or `ldapadd` for
instance.

### Onsite

Onsite backups are pretty simple, all that needs to be done is to go to `hal`
and find the backup to restore from in `/opt/backups/live`. All backups of
recent data are found in either `rsnapshot` (for daily backups) or `misc` (for
any incidents or one-off backups). Within `rsnapshot`, the backups are
organized into directories dependings on how long ago the backup was made. To
see when each backup was created just use `ls -l` to show the last modified
time of each directory.

### Offsite

Offsite backups are more complicated because the backup files first need to be
downloaded, stuck together into a single file, decrypted, extracted, and then
put into LVM to get back the whole backup archive that would normally be found
onsite. This essentially just means that the
[create-encrypted-backup][create-encrypted-backup] script needs to be reversed
to restore once the backup files are downloaded. Here are the general steps to
take to restore from an offsite backup:

1. Download all the backup pieces from Box.com. This is generally easiest with
   a command line tool like `cadaver`, which can just use a `mget *` to download
   all the files (albeit sequentially). If more speed is needed, open multiple
   `cadaver` connections and download multiple groups of files at once.

2. Put together all the backup pieces into a single file. This can be done by
   running `cat <backup>.img.gz.gpg.part* > <backup>.img.gz.gpg`.

3. Decrypt the backup using `gpg`. This requires your key pair to be imported
   into `gpg` first using `gpg --import public_key.gpg` and
   `gpg --allow-secret-key-import --import private_key.gpg`, then you can
   decrypt the backup with
   `gpg --output <backup>.img.gz --decrypt <backup>.img.gz.gpg`. Be careful to
   keep your private key secure by setting good permissions on it so that nobody
   else can read it, and delete it after the backup is imported. The keys can be
   deleted with `gpg --delete-secret-keys "<Name>"` and
   `gpg --delete-key "<Name>"`, where your name is whatever name it shows when
   you run `gpg --list-keys`.

4. Extract the backup with `gunzip <backup>.img.gz`.

5. Put the backup image into a LVM logical volume. First find the size that the
   volume should be by running `ls -l <backup>.img`, and copy the number of
   bytes that outputs. Then create the LV with
   `sudo lvcreate -L <bytes>B -n <name> /dev/<volume group>` where the volume
   group has enough space to store the entire backup (2+ TiB).

## Backup Contents

Backups currently include:

* Everything on NFS
  * User home and web directories
  * Cronjobs on supported servers (tsunami, supernova, biohazard, etc.)
* MySQL databases (including user databases, stats, RT, print quotas, IRC data)
* Everything on GitHub (probably very unnecessary)
* LDAP and Kerberos data
* A [smattering of random files on random servers][backed-up-files]

## Backup Procedures

Backups are currently made daily via a cronjob on `hal` which calls `rsnapshot`.
The current settings are to retain 7 daily backups, 4 weekly backups, and 6
monthly backups, but we might adjust this as it takes more space or we get
larger backup drives.

We use `rsnapshot` to make incremental backups. Typically, each new backup
takes an additional ~3GiB of space (but this will vary based on how many files
actually changed). A full backup is about ~2TiB of space and growing.

(The incremental file backups are only about ~300 MiB, but since mysqldump
files can't be incrementally backed up, those take a whole ~2 GiB each time, so
the total backup grows by ~3GiB each time. However, an old backup is discarded
each time too, so it approximately breaks even.)

## Ideas for backup improvements

1. Automate backup testing, so have some system for periodically checking that
   backups can be restored from, whether they are offsite or onsite.

[box]: https://www.box.com
[create-encrypted-backup]: https://github.com/ocf/puppet/blob/master/modules/ocf_backups/files/create-encrypted-backup
[upload-to-box]: https://github.com/ocf/puppet/blob/master/modules/ocf_backups/files/upload-to-box
[backed-up-files]: https://github.com/ocf/puppet/blob/17bc94b395e254529d97c84fb044f76931439fd7/modules/ocf_backups/files/rsnapshot.conf#L53
