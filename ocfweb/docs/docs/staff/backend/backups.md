[[!meta title="Backups"]]
## Backup Storage

We have two sources of storage for on-site backups:

* `pandemic:/opt/backups` (2 TiB usable; 2x 2-TiB WD RE drives in RAID 1)

  These drives serve as the primary backup location. New backups are saved
  here.

* `hal:/opt/backups` (2 TiB usable; 2x 1-TiB WD RE drives in RAID 0)

  These drives are a secondary backup location, and are cloned daily from the
  same location on `pandemic`.

## Off-Site Backups

There is a single 2-TiB WD RE drive used for off-site backup storage. It's
encrypted (`LUKS`) and stored in the SM's apartment (with a password known only
to the GM/SM).

A more sophisticated scheme for off-site backups might be preferable at some
point. Cloud-based storage is usually far too expensive (e.g. Glacier can
easily cost thousands of dollars, see rt#253).

[TODO: Re-evaluate cost with Google Nearline? But it's probably still too
expensive.]

## Backup Contents

Backups currently include:

* Everything on NFS
  * User home and web directories
  * `/opt/ocf` (some scripts and common environment settings)
* MySQL databases (including user databases, stats, RT, print quotas)

## Backup Procedures

Backups are currently made daily via a cronjob on `pandemic` which calls
rsnapshot. The current settings are to retain 7 daily backups, 4 weekly
backups, and 6 monthly backups, but we might adjust this as we find out how
much space that takes.

We use `rsnapshot` to make incremental backups. Typically, each new backup
takes an additional ~3GiB of space (but this will vary based on how many
files actually changed). A full backup is about ~700GiB of space.

(The incremental file backups are only about ~300 MiB, but since mysqldump
files can't be incrementally backed up, those take a whole ~2 GiB each time.)

#### Request Tracker

The RT database is stored in the `ocfrt` database on the MySQL host. It should
be possible to restore RT using just the database, but nobody has tested
restoring these.

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

7. Come up with some rotation for off-site backups so at all times one is with
   SM, and one is in server room. This makes it easier to keep the off-site
   backup relatively recent.

7. Investigate whether cloud-based is viable (probably not)
