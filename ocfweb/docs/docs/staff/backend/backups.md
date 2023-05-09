[[!meta title="Backups"]]
## Backup Storage

We currently store our on-site backups across a RAID mirror on `hal`:

* `hal:/backup` (16 TB usable; 2x 16 TB WD drives in ZFS mirror)

Backups are stored as ZFS snapshots. ZFS snapshots have the advantage of being
immutable, browsable, and they can be sent to other ZFS pools for off-site
backups.

## Off-Site Backups

Todo: new off-site backup documentation.

## Restoring Backups

The easiest way to restore from a backup is to look at how it is made and
reverse it. If it is a directory specified in rsnapshot, then likely all that
needs to be done is to take that directory from the backup and put it onto the
server to restore onto. Some backups, such as mysql, ldap, and kerberos are more
complicated, and need to be restored using `mysqlimport` or `ldapadd` for
instance.

### Onsite

Compared to the old setup, onsite backups are a little harder to find.They are
located at `/backup/encrypted/rsnapshot` on `hal`. In addition, we have a
dataset for each top-level user directory, such as `/home/a/`, which is stored
as the `backup/encrypted/rsnapshot/.sync/nfs/opt/homes/home/a` dataset.

The ZFS snapshots are stored in the `.zfs/snapshot` directory of each dataset.
The `.zfs` folder is hidden and will not show up even with the `ls -a` command,
so you will need to manually `cd` into the directory. The snapshots are time-
stamped, so you can find the snapshot you want to restore from by looking at the
date string in the snapshot name. For example, if you wanted to restore the
`public_html` directory of user `foo` with the backup from 2023-05-01, you
should enter the 
```
/backup/encrypted/rsnapshot/.sync/nfs/opt/homes/services/http/users/f/.zfs
```
directory, and then go inside the `snapshot/` folder. From there, you enter the
`zfs-auto-snap_after-backup-2023-05-01-1133/` directory (note that the time is
UTC), and then you can copy the `foo/` directory to the user's home directory.

For large directories, please use `/backup/encrypted/scratch` as a temporary
working area for compressing the files and other operations. Please note that
this dataset will not be automatically snapshotted.

MySQL backups are stored at the `/backup/encrypted/rsnapshot/mysql/` directory,
and the snapshots can be accessed at
`/backup/encrypted/rsnapshot/mysql/.zfs/snapshot/`. Inside a snapshot, the
individual databases are stored as `.sql` files inside the `.sync/` directory.

### Offsite

Todo: add instructions for restoring offsite backups using zfs send/receive.

## Backup Contents

Backups currently include:

* Everything on NFS
  * User home and web directories
  * Cronjobs on supported servers (tsunami, supernova, biohazard, etc.)
* MySQL databases (including user databases, stats, RT, print quotas, IRC data)
* A few OCF repositories on GitHub (probably very unnecessary)
* LDAP and Kerberos data
* A [smattering of random files on random servers][backed-up-files]

## Backup Procedures

Backups are currently made daily via a cronjob on `hal` which calls `rsnapshot`.

We use `rsnapshot` and ZFS snapshots to make incremental backups. Typically,
each new backup takes an additional ~20GiB of space (but this will vary based on
how many files actually changed). A full backup is about ~4TiB of space and
growing.

(The incremental file backups are only about ~1-5 GiB, but since MySQL and
Postgres files can't be incrementally backed up, those take a whole ~ 15 GiB
each time, so the total backup grows by ~20GiB each time.)

## Ideas for backup improvements

1. Automate backup testing, so have some system for periodically checking that
   backups can be restored from, whether they are offsite or onsite.

[rsyncnet]: https://www.rsync.net
[create-encrypted-backup]:
    https://github.com/ocf/puppet/blob/master/modules/ocf_backups/files/create-encrypted-backup
[upload-to-box]:
    https://github.com/ocf/puppet/blob/master/modules/ocf_backups/files/upload-to-box
[backed-up-files]:
    https://github.com/ocf/puppet/blob/17bc94b395e254529d97c84fb044f76931439fd7/modules/ocf_backups/files/rsnapshot.conf#L53
[prune-old-backups]:
    https://github.com/ocf/puppet/blob/master/modules/ocf_backups/files/prune-old-backups
