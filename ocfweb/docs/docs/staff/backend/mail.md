[[!meta title="Mail"]]
# Mail

We maintain two mail servers:

* **anthrax**, used for sending and receiving nearly all mail. Mail sent by
  users, websites, or basically anything else goes through here.

  Received mail to @ocf.berkeley.edu is looked up via LDAP (or the aliases
  table) and forwarded or rejected; nothing is stored.

  Mail originating anywhere inside OCF relays through anthrax.

* **sandstorm**, used for receiving and forwarding mail for groups with virtual
  hosts. sandstorm sends no mail itself; even forwarded mail gets relayed
  through anthrax.

  Originally, sandstorm handled all mail. But the config was scary and not
  documented or in Puppet (this is still the case). We hope to eventually
  change this (unsure whether that means consolidating to a single server or
  not, though).


## External relations

We maintain relations with external groups for two reasons.

 1. To monitor our mail server reputation and prevent outgoing mail from
    being blocked by external service providers.
 2. To monitor abuse and disable compromised accounts.

When our IP addresses change, we need to update our registrations.

We have
[feedback loops](https://en.wikipedia.org/wiki/Feedback_loop_%28email%29)
with

 - AOL
 - Comcast (out-of-date)
 - Cox (out-of-date)
 - FastMail (out-of-date)
 - Microsoft (Junk Email Reporting Agreement, 2013-03-06) (out-of-date)
 - Rackspace (out-of-date)
 - RoadRunner (out-of-date)
 - Yahoo

We are whitelisted by

 - AOL (out-of-date)
 - [DNSWL](https://www.dnswl.org/s/?s=berkeley.edu)
 - Verizon (out-of-date)

We are also registered with

 - [abuse.net](http://abuse.net/lookup.phtml?domain=ocf.berkeley.edu)
 - SpamCop (ISP account set to receive summary reports)
