[[!meta title="Virtual hosting (staff)"]]
## Policy checklist

* Website developed, not a placeholder
* Website hosted substantially on the OCF
* Website has required university disclaimer on every page
* Website has hosted by OCF banner on the front page that is noticeable without undue effort and links to the OCF home page
* Request is made by a registered and active student organization in CalLink (LEAD Center) or request is sponsored by an [administrative official](http://compliance.berkeley.edu/delegation/principles)
* Group does not already have a virtual host, or has an exception from the Board of Directors


## Enabling virtual hosting
### Web

Edit the file `~staff/vhost/vhost.conf`, adding a new line. The format is
documented at the top.

This takes effect at the top of every hour when a cronjob runs. HTTPS takes
about an additional hour to take effect (for the first hour, it will be
HTTP-only).

If mail is also requested, skip to the next section. Otherwise, request the
following DNS record from the
[University hostmaster](http://www.net.berkeley.edu/hostmaster/):

    hostname.berkeley.edu. IN CNAME death.ocf.berkeley.edu.

Use the domain requested by the group in place of `hostname`. We have a
[reusable email template](http://templates.ocf.berkeley.edu/#hostmaster-new-domain)
for making new DNS requests.

### Mail (if requested)    {mail}

Edit the file `~staff/vhost/vhost-mail.conf`, adding a new line for the group.
The format is simply:

    groupname domainname

This immediately takes effect, allowing the group to [[edit their email config|vhost_mail]]
(and the mail server will start accepting incoming/outgoing mail), but you
still need to update the DNS so that they can actually receive mail.

If the group already has virtual hosting for their website, which is likely the
case, request from the [University hostmaster](http://www.net.berkeley.edu/hostmaster/)
that the following DNS record be dropped:

    hostname.Berkeley.EDU. IN CNAME death.OCF.Berkeley.EDU.

Then, whether or not the group has web virtual hosting, request the following DNS records:

    hostname.Berkeley.EDU. IN A 169.229.226.23
    hostname.Berkeley.EDU. IN MX 5 anthrax.OCF.Berkeley.EDU.

Use the domain requested by the group in place of `hostname`. We have a
[reusable email template](http://templates.ocf.berkeley.edu/#hostmaster-add-mail)
for making DNS mail requests.


### Application hosting
The group website should be reasonably developed (can be offsite during review only for this request) before approving it.

You will need a `/admin` principle to modify apphosting entries.

* Add the group account to the ocfdev LDAP group:

      $ ldapvi cn=ocfdev
      memberUid: ggroup
      memberUid: GROUP_USERNAME

* Add apphost entry: edit `~staff/vhost/vhost-app.conf`. The file syntax is

      account vhost_name socket_name ssl_name

  The config file contains examples and more documentation.

* Wait for cronjob to update configurations (runs every 10 minutes).

Once the cronjob completes, the application will be available at:

    VHOST_NAME-berkeley-edu.apphost.ocf.berkeley.edu

VHOST_NAME is the configured name from above.

Once the website is developed and meets policy checklist, request the following DNS record from the [University hostmaster](http://www.net.berkeley.edu/hostmaster/):

    hostname.berkeley.edu. IN CNAME werewolves.OCF.Berkeley.EDU

The nginx running on apphosting server will return a `502 Bad Gateway` or actual content if the apphost is configured properly, and a `403 Forbidden` otherwise.
