[[!meta title="Virtual hosted mail"]]

**Note: This page is designed for OCF staffers and is a technical description
of the service. For information or help using it, see [[our page about it|doc
services/vhost/mail]].**

Virtual hosting mail allows groups to receive mail at `@group.b.e` addresses,
and send from those same addresses. It complements our web hosting nicely.

## Features

* Each user has mail forwarding.

* Each virtual user can have its own password (not the same as the account
  password). If a user doesn't have a password set, then they can receive mail
  but not send it.

* [[Simple admin panel|vhost_mail]] built into ocfweb for admins to set
  passwords for emails.  It might also be cool if you could change your own
  password (without having the group password), but that's not currently
  possible.


## Technical implementation

There is a database on our MySQL host for storing email vhost information. It
has one table, `addresses`, with columns for the incoming address, password,
and forwarding addresses (among others).

It has one view, `domains`, which is generated from the `addresses` table. This
is only used to make the queries Postfix makes simpler. In particular, you
never need to update MySQL to add forwarding to a domain; it's entirely based
on `~staff/vhost/vhost-mail.conf`.

ocflib has simple functions for interacting with this database (see `pydoc3
ocflib.vhost.mail`).

We use MySQL lookup tables on the mail host to dynamically look up the list of
virtual domains (using the `domains` view), and the addresses (using the
`addresses` table).

For sending, we use pam-mysql to authenticate SMTP sessions before allowing
clients to send as a vhost address. (See `/etc/pam.d/smtp` and
`/etc/pam-mysql.conf` on anthrax).


## How do I add mail hosting to a group?

See [[here|doc staff/howto/user-services/vhost#mail]].
