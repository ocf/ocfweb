[[!meta title="Backups"]]
## Backup Storage

We currently store our on-site backups across a couple drives on `hal`:

* `hal:/opt/backups` (6 TiB usable; 2x 3-TiB WD RE drives in an LVM volume group)

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

We also use Google Nearline on an ad-hoc basis (i.e. we have scripts to make
the backup, but they only upload and don't remove the old backups). They're
not yet executed automatically and require some human care to ensure things
work properly.


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

Backups are currently made daily via a cronjob on `hal` which calls rsnapshot.
The current settings are to retain 7 daily backups, 4 weekly backups, and 6
monthly backups, but we might adjust this as it takes more space or we get
larger backup drives.

We use `rsnapshot` to make incremental backups. Typically, each new backup
takes an additional ~3GiB of space (but this will vary based on how many
files actually changed). A full backup is about ~1.3TiB of space and growing.

(The incremental file backups are only about ~300 MiB, but since mysqldump
files can't be incrementally backed up, those take a whole ~2 GiB each time,
so the total backup grows by ~3GiB each time.)

#### Request Tracker

The RT database is stored in the `ocfrt` database on the MySQL host. It is
possible to restore RT using just the database; in fact, simply running
puppet is now sufficient to bring up a fully-functioning RT server.

## Ideas for backup improvements

Some general ideas for improving backups:

1. **Done.** Use RAID 0 on `hal:/dev/sdb` to get an effective 2 TiB of space,
   matching pandemic. Mirror the two (pandemic -> hal); pandemic is master.

   (pandemic already does RAID 1, so the chance of that failing the same time a
   hal drive fails without some external disaster which destroys the entire
   server rack is low.)

2. **Done.** Make the backup on hal automatically clone the backup on pandemic
   periodically. Should find a way to make it happen only when no backups are
   going on (which might be hard, since copying all the files takes a long
   time -- about 7.25 hours).

   Currently there is a script `hal:/opt/copy-backups.sh`, but we need some
   more complicated setup than just putting it in cron (it requires SSHing to
   pandemic as password, which can't be automated).

3. **Done.** Use incremental file backups, possibly rsnapshot

4. **Done.** Backup certain directories on servers

     * Crontabs
     * LDAP
     * Kerberos
     * Puppet shares and master's directory (has puppet CA)
     * Munin records (`stats:/var/lib/munin`)
     * DNS zones (`ns:/etc/bind`; we should just move this to git)
     * *more things here* (feel free to add)

5. **Done.** Backup git repositories (currently mostly on GitHub)

6. **Done.** Automate the backups and rotation.

7. **Done.** Automate weekly offsite backups to Box.

8. Automate backup testing, so have some system for periodically checking that
   backups can be restored from, whether they are offsite or onsite.

9. Possibly automate offsite backups to Google Nearline? This is probably
   unnecessary given that there are already offsite backups on Box and we'd
   have to pay for this.

[box]: https://www.box.com
[create-encrypted-backup]: https://github.com/ocf/puppet/blob/master/modules/ocf_backups/files/create-encrypted-backup
[upload-to-box]: https://github.com/ocf/puppet/blob/master/modules/ocf_backups/files/upload-to-box
[backed-up-files]: https://github.com/ocf/puppet/blob/master/modules/ocf_backups/files/rsnapshot.conf#L53
