[[!meta title="Configuring virtual hosting"]]

## Policy checklist

* Website developed, not a placeholder
* Website hosted substantially on the OCF
* For RSOs, website has required university disclaimer on every page
* Website has hosted by OCF banner on the front page that is noticeable without
  undue effort and links to the OCF home page
* Request is made by a registered and active student organization in CalLink
  (LEAD Center), request is sponsored by an [administrative
  official](https://compliance.berkeley.edu/delegation/principles), or request
  is for the account of a faculty or staff member
* For RSOs, request is made by a signatory of the group in question (use
  `signat group <group>` to see signatories)
* For faculty/staff, the requestor has already obtained a domain from e.g.
  their department
* Account does not already have a virtual host, or has an exception from a Site
  Manager
* For RSOs, domain name complies with [LEAD Center guidelines](https://lead.berkeley.edu/wp-content/uploads/2014/12/student-org-domain-guidelines.pdf). In
  particular, requested domain name is sufficiently similar to their official
  name and wouldn't potentially be confused with a university department.
* For non-berkeley.edu domains, domain name has been approved by a (D)GM or
  (D)SM. (We wish to keep the number of these domains under check to limit the
  number of non-berkeley.edu domain owners we have to contact when our web
  server or mail server DNS changes.)


## Enabling virtual hosting

### Web

Edit the file `configs/vhost.conf` in the [`ocf/etc` repo][ocf-etc], adding new
entries at the top. The format is documented at the top of that file.

This takes effect at the top of every hour when a cronjob runs. HTTPS should
available shortly afterwards (within 5-10 minutes). Keep in mind that vhosts
are not available without HTTPS, so there may be a short period of time where
the new vhost is unavailable or giving a certificate error.

Next, request the following DNS records from the [University
hostmaster][campus-hostmistress]:

    hostname.berkeley.edu. IN CNAME hosting.ocf.berkeley.edu

Use the domain requested by the group in place of `hostname`. We have a
[reusable email
template](https://templates.ocf.berkeley.edu/#hostmaster-new-domain) for making
new DNS requests. This email should be sent to hostmaster@nic.berkeley.edu
and sm+vhost@ocf.berkeley.edu.

Answers to the following questions (provided by the requestor of the subdomain)
should be sent to the University hostmaster along with the DNS request itself.
1. The purpose of the hostname, who will be using it, and its relationship to the university's mission

2. A responsible contact for the hostname

3. Acknowledgment that all relevant university policies will be followed, including those pertaining to [campus website accessibility][campus-accessibility]


### Mail (if requested)    {mail}

Edit the file `configs/vhost-mail.conf` in the [`ocf/etc` repo][ocf-etc],
adding a new line for the group at the top of the file. The format is simply:

    groupname domainname

This takes effect after around 30 minutes (once puppet has run and synced
ocf/etc), allowing the group to [[edit their email config|vhost_mail]] (and the
mail server will start accepting incoming/outgoing mail), but you still need to
update the DNS so that they can actually receive mail.

We request the same DNS records for mail hosting as for web hosting. First,
check if any DNS records already exist with

    dig hostname.berkeley.edu A AAAA MX

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

Mail virtual hosting may be requested separately from website virtual hosting and without a completely developed website.


### Application hosting

The group website should be reasonably developed (can be offsite during review
only for this request) before approving it.

You will need a `/admin` principal to modify apphosting entries.

* Add the group account to the ocfapphost LDAP group:

      $ ldapvi cn=ocfapphost
      memberUid: ggroup
      memberUid: GROUP_USERNAME

* Add a new apphost entry to the top of `configs/vhost-app.conf` in the
  [`ocf/etc` repo][ocf-etc]. The file syntax is:

      account vhost_name socket_name ssl_name

  The config file contains examples and more documentation.

* Wait for puppet to sync `/etc/ocf` and for the cronjob to update
  configurations (runs every 10 minutes).

Once the cronjob completes, the application will be available at:

    VHOST_NAME-berkeley-edu.apphost.ocf.berkeley.edu

`VHOST_NAME` is the configured name from above.

Once the website is developed and meets policy checklist, request the following
DNS record from the [University hostmaster][campus-hostmistress]:

    hostname.Berkeley.EDU. IN A 169.229.226.49
    hostname.Berkeley.EDU. IN AAAA 2607:f140:8801::1:49
    hostname.Berkeley.EDU. IN MX 5 anthrax.OCF.Berkeley.EDU.

Remember to request that any existing records be dropped as well. You can check
for records with `dig hostname.berkeley.edu [A|AAAA|MX]`. The nginx running on
apphosting server will return a `502 Bad Gateway` or actual content if the
apphost is configured properly, and a `403 Forbidden` otherwise.

[ocf-etc]: https://github.com/ocf/etc
[campus-hostmistress]: https://ucb.service-now.com/kb_view.do?sysparm_article=KBT0012470
[campus-accessibility]: https://dac.berkeley.edu/web-accessibility
