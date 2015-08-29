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

Request the following DNS record from the [University hostmaster](http://www.net.berkeley.edu/hostmaster/) (unless mail is also requested, in that case, skip to the next section):

    vhost.berkeley.edu. IN CNAME death.ocf.berkeley.edu.

### Mail (if requested)

* Add vhost: edit `~staff/vhost/vhost-mail.conf`.
* Update vhost configuration: Run `sudo ~staff/vhost/buildvirtual-mail.sh` on sandstorm.
* Reload vhost configuration: run `sudo service postfix reload` on sandstorm.

Request the following DNS records from the [University hostmaster](http://www.net.berkeley.edu/hostmaster/):

    vhost.berkeley.edu. IN A 169.229.10.23
    vhost.berkeley.edu. IN MX 5 sandstorm.ocf.berkeley.edu.
