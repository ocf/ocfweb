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

* Add vhost: edit `~staff/vhost/vhost.conf`.
* Update vhost configuration and restart Apache: run `sudo ~staff/vhost/web.sh` on death.

If mail is also requested, skip to the next section. Otherwise, request the following DNS record from the [University hostmaster](http://www.net.berkeley.edu/hostmaster/):

    hostname.berkeley.edu. IN CNAME death.ocf.berkeley.edu.

Use the domain requested by the group in place of `hostname`. We have a [reusable email template](http://templates.ocf.berkeley.edu/#hostmaster-new-domain) for making new DNS requests.

### Mail (if requested)

* Add vhost: edit `~staff/vhost/vhost-mail.conf`.
* Update vhost configuration: Run `sudo ~staff/vhost/mail.sh` on sandstorm.

If the group already has virtual hosting for their website, which is likely the case, request from the [University hostmaster](http://www.net.berkeley.edu/hostmaster/) that the following DNS record be dropped:

    hostname.Berkeley.EDU. IN CNAME death.OCF.Berkeley.EDU.

Then, whether or not the group has web virtual hosting, request the following DNS records:

    hostname.Berkeley.EDU. IN A 169.229.226.23
    hostname.Berkeley.EDU. IN MX 5 sandstorm.OCF.Berkeley.EDU.

Use the domain requested by the group in place of `hostname`. We have a [reusable email template](http://templates.ocf.berkeley.edu/#hostmaster-add-mail) for making DNS mail requests.
