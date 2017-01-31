[[!meta title="Mail hosting for student groups"]]


Our regular virtual hosting gives your group a website at
`mygroup.berkeley.edu`. By contrast, *mail virtual hosting* lets you create as
many email addresses as you'd like `@mygroup.berkeley.edu`.

These addresses can be used both to receive mail (via mail forwarding), and
send mail. The details of how to use these addresses are below.


## Getting set up with mail virtual hosting

By default, groups only have regular web virtual hosting.

If you'd like to get started using mail virtual hosting, send us an email at
[hostmaster@ocf.berkeley.edu](mailto:hostmaster@ocf.berkeley.edu) letting us
know you'd like to enable email virtual hosting. Be sure to include both the
domain name, and your OCF account name.

Once your domain is configured for mail hosting, head over to our [[mail
virtual hosting page|vhost_mail]] to add and remove addresses.


## How sending and receiving mail works

In the past, we provided a full mail service, including storing mail on our
servers. However, we found that few groups actually wanted this. Most people
are already juggling multiple email addresses, and don't particularly want
another mailbox to monitor.

Instead, we now provide *mail forwarding* for incoming mail, and *mail sending*
for outgoing mail. This means that incoming mail will always be forwarded to
some other address (such as your berkeley.edu address or your personal Gmail),
but you can always send mail using your `@mygroup.berkeley.edu` address.

This is super convenient: you don't have to manage a separate inbox, but you
can still compose mail or reply to mail as your fancy group email, even from
your phone.

We provide instructions for setting this up with Gmail below, but other email
providers and clients offer similar options.


#### How can I use Gmail to send and receive email?

[[We have an entire page about that — click here!|doc
services/vhost/mail/gmail]]


#### How can I use an email client besides Gmail to send and receive email?

There are too many email clients for us to provide instructions for, so here
are the settings you'll need:

* **SMTP server:** `smtp.ocf.berkeley.edu`
* **Port:** 587
* **Security:** TLS, verify cert
* **Username:** The full email address, including domain name
* **Password:** The password you set

Note that we *only provide email sending*, so you only need to configure SMTP
and not POP/IMAP.

Good luck!



#### What if I only want to receive and not send email?

You can totally do that! Just set up an address to forward to and don't bother
configuring the sending address. You can even leave the password blank.
