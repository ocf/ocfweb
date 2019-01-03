[[!meta title="Configuring virtual hosting"]]

## Policy checklist

* Website developed, not a placeholder
* Website hosted substantially on the OCF
* For RSOs, website has required university disclaimer on every page
* Website has hosted by OCF banner on the front page that is noticeable without
  undue effort and links to the OCF home page
* Request is made by a registered and active student organization in CalLink
  (LEAD Center), request is sponsored by an [administrative
  official](http://compliance.berkeley.edu/delegation/principles), or request
  is for the account of a faculty or staff member
* For RSOs, request is made by a signatory of the group in question (use
  `signat group <group>` to see signatories)
* For faculty/staff, the requestor has already obtained a domain from e.g.
  their department
* Account does not already have a virtual host, or has an exception from a Site
  Manager
* For RSOs, domain name complies with [LEAD Center guidelines](http://lead.berkeley.edu/wp-content/uploads/2014/12/student-org-domain-guidelines.pdf). In
  particular, requested domain name is sufficiently similar to their official
  name and wouldn't potentially be confused with a university department.
* For non-berkeley.edu domains, domain name has been approved by a (D)GM or
  (D)SM. (We wish to keep the number of these domains under check to limit the
  number of non-berkeley.edu domain owners we have to contact when our web
  server or mail server DNS changes.)


## Enabling virtual hosting

### Web

Edit the file `~staff/vhost/vhost.conf`, adding a new line. The format is
documented at the top.

This takes effect at the top of every hour when a cronjob runs. HTTPS takes
about an additional hour to take effect (for the first hour, it will be
HTTP-only).

Next, request the following DNS records from the [University
hostmaster](http://www.net.berkeley.edu/hostmaster/):

    hostname.Berkeley.EDU. IN A 169.229.226.23
    hostname.Berkeley.EDU. IN AAAA 2607:f140:8801::1:23
    hostname.Berkeley.EDU. IN MX 5 anthrax.OCF.Berkeley.EDU.

Use the domain requested by the group in place of `hostname`. We have a
[reusable email
template](https://templates.ocf.berkeley.edu/#hostmaster-new-domain) for making
new DNS requests.

### Mail (if requested)    {mail}

Edit the file `~staff/vhost/vhost-mail.conf`, adding a new line for the group.
The format is simply:

    groupname domainname

This immediately takes effect, allowing the group to [[edit their email
config|vhost_mail]] (and the mail server will start accepting incoming/outgoing
mail), but you still need to update the DNS so that they can actually receive
mail.

We request the same DNS records for mail hosting as for web hosting. First,
check if any DNS records already exist with

    dig hostname.berkeley.edu [A|AAA|MX]

for IPv4/IPv6/mail records, respectively. If they have all the records from the
previous section, you don't have to do anything else.

If not, make the same request to the University hostmaster as in the previous
section. If you see this record:

    hostname.Berkeley.EDU. IN CNAME death.OCF.Berkeley.EDU.

then include in your request to the hostmaster that it be dropped.

We have a
[reusable email
template](https://templates.ocf.berkeley.edu/#hostmaster-add-mail) for making
DNS mail requests for groups that have old `CNAME` records.


### Application hosting

The group website should be reasonably developed (can be offsite during review
only for this request) before approving it.

You will need a `/admin` principal to modify apphosting entries.

* Add the group account to the ocfapphost LDAP group:

      $ ldapvi cn=ocfapphost
      memberUid: ggroup
      memberUid: GROUP_USERNAME

* Add apphost entry: edit `~staff/vhost/vhost-app.conf`. The file syntax is

      account vhost_name socket_name ssl_name

  The config file contains examples and more documentation.

* Wait for cronjob to update configurations (runs every 10 minutes).

Once the cronjob completes, the application will be available at:

    VHOST_NAME-berkeley-edu.apphost.ocf.berkeley.edu

`VHOST_NAME` is the configured name from above.

Once the website is developed and meets policy checklist, request the following
DNS record from the [University
hostmaster](http://www.net.berkeley.edu/hostmaster/):

    hostname.Berkeley.EDU. IN A 169.229.226.49
    hostname.Berkeley.EDU. IN AAAA 2607:f140:8801::1:49
    hostname.Berkeley.EDU. IN MX 5 anthrax.OCF.Berkeley.EDU.

Remember to request that any existing records be dropped as well. You can check
for records with `dig hostname.berkeley.edu [A|AAAA|MX]`. The nginx running on
apphosting server will return a `502 Bad Gateway` or actual content if the
apphost is configured properly, and a `403 Forbidden` otherwise.
