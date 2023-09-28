[[!meta title="Mail"]]

**anthrax** is our mail server. It is used for sending and receiving all OCF
mail, excluding staff use of Google Apps. Mail sent by users, websites, virtual
hosts, or basically anything else goes through here.

Received mail to @ocf.berkeley.edu is forwarded to the address in the `mail`
attribute of the LDAP account entry (or the [aliases
table](https://github.com/ocf/puppet/blob/master/modules/ocf_mail/files/site_ocf/aliases))
or rejected; nothing is stored.

Received virtual host mail is forwarded to the address stored in a MySQL table.
Outgoing virtual host mail is also via anthrax, which uses SMTP authentication
(passwords checked against `crypt(3)`'d passwords in a MySQL table). [[There's a
whole page with more details about vhost mail.|doc staff/backend/mail/vhost]]

Mail originating anywhere inside the OCF relays through anthrax.


## External relations

We maintain relations with external groups for two reasons.

 1. To monitor our mail server reputation and prevent outgoing mail from being
    blocked by external service providers.
 2. To monitor abuse and disable compromised accounts.

When our IP addresses change, we need to update our registrations.

We have [feedback
loops](https://en.wikipedia.org/wiki/Feedback_loop_%28email%29) with

 - AOL (out-of-date)
 - Comcast (out-of-date)
 - Cox (out-of-date)
 - FastMail (out-of-date)
 - Microsoft (Junk Email Reporting Agreement, 2013-03-06) (out-of-date)
 - Rackspace (out-of-date)
 - RoadRunner (out-of-date)
 - Yahoo (out-of-date)

We are whitelisted by

 - AOL (out-of-date)
 - [DNSWL](https://www.dnswl.org/s/?s=berkeley.edu) (out-of-date)
 - Verizon (out-of-date)

We are also registered with

 - [abuse.net](https://www.abuse.net/lookup.phtml?domain=ocf.berkeley.edu)
 - SpamCop (ISP account set to receive summary reports)
