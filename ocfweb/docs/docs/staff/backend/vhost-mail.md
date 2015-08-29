[[!meta title="Plans for new vhost mail server"]]
# Plans for new vhost mail server

We want to provide better mail for virtually-hosted student groups. There's
probably a lot of demand for this service, and it complements our web hosting
nicely.

Comments on this document are greatly appreciated before the actual technical
work begins.

## Desired features

In rough order of importance:

* Ability to configure virtual users for a domain.

* Each user can have mail forwarding, if they want it

* Each user can have mail storage (IMAP, webmail) and mail sending (SMTP,
  webmail)

* Each virtual user has its own password (not the same as the account password)

* Simple admin panel built into atool for admins to set passwords for emails.
  It might also be cool if you could change your own password (without having
  the group password), but that's low priority.

* Ability to set up mailing lists (*maybe*... I think campus covers this pretty
  well already, so not sure it's worth the additional trouble. Certainly not
  during the initial iteration of the new service.)

## Technical implementation

This satisfies all features except mailing lists, which we might not do.

1. Set up a new server (to replace `sandstorm`); referred to as `sandstorm`
   from now on.

2. Set up a database on `maelstrom` for storing email vhost information.
   Postfix, Dovecot, etc. have good support for MySQL.

   The database will contain information about vhost domains, vhost users
   (password hashes, mail storage/forwarding).

   Not entirely sure what the schema will look like yet, but this is definitely
   possible (I've done something similar before).

3. Write simple functions (in ocflib) for interacting with the database.
   They'll be functions like:

        list_domains(cred)
        add_domain(cred, domain)
        add_user(cred, domain, user, password)
        change_password(cred, domain, user, new_password)

   ...which accept `cred` (MySQL credentials), which will be stored in the
   `atool` config (and maybe on `supernova` readable by `ocfstaff`, if we write
   simple command-line tools for adding vhosts).

4. Create `/services/mail/` (on NFS) to hold Maildirs. Suggested layout is like
   `/services/mail/vhost/$domain/$user/Maildir/`, but not sure if the last `Maildir`
   is necessary (will we ever want to store other things here?).

5. Set up Postfix, Dovecot on `sandstorm` interacting with the MySQL (via a
   read-only password)

6. Set up Roundcube on `death` (webmail)

7. Set up simple web UI for the ocflib functions as part of `atool`. We already
   have most of the hard bits (like authenticating users), so we just need to
   write a little CRUD.

8. Provide nifty instructions on wiki for linking with iOS, Android, Gmail,
   Thunderbird.
