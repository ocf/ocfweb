[[!meta title="Virtual hosting (group.berkeley.edu)"]]


Virtual hosting allows group accounts to have their website available on a
different domain, typically under berkeley.edu. For example, a group's site can
be made available at `yourgroup.berkeley.edu` in addition to the standard
address under `ocf.berkeley.edu`.

The OCF provides two separate (but related) virtual hosting services:

* **Web hosting**, where your group's OCF-hosted website becomes available
  under the new name

* **Email forwarding**, which lets you configure email forwarding for the new
  name

Web hosting is always enabled for group accounts with virtual hosting, but
email forwarding must be requested separately.

## Web Hosting

After the virtual host is set up, the files in the `public_html` directory of
your group account (ordinarily accessible at
`https://www.ocf.berkeley.edu/~accountname`) will appear at the root directory
of the virtual-hosted site (`yourgroup.berkeley.edu`).

### Instructions

1.   **Request group account.** [[Request an OCF group account|doc membership]]
     (if you haven't already done so).
2.   **Set up real site.** Set up your webspace and upload your website (if you
     haven't already done so). The website should be developed already, not a
     placeholder.
3.   **Include OCF hosting banner.** Place a [[Hosted by OCF banner|doc
     services/vhost/badges]] on your home page that links to the OCF front
     page. If none of these images are appropriate for your site, you may
     design one of your own and [[submit it|doc contact]] for approval.
4.   **Include university's disclaimer (if applicable).** If you are a student
     group, place the university-mandated student group disclaimer on each page
     of your website (see the section below).
5.   **Complete request form.** Complete the [[virtual hosting request
     form|request_vhost]] online. OCF staff will review your request and
     contact the university hostmaster on your behalf.

### Including the OCF banner

Place any of the [[Hosted by OCF banners|doc services/vhost/badges]] on your
site by copying the code onto your page. The banner is required to be placed
only on the home page of your site. You can also create your own OCF banner
with approval from the OCF (see instructions above).

### Including the University Student Group Disclaimer    {disclaimer}

The university [requires][rso-domains] that all student group websites on a
subdomain of berkeley.edu (other than those of university-sponsored student
groups) contain the following text on each page:

> We are a student group acting independently of the University of California.
> We take full responsibility for our organization and this web site.

### Policies

#### Groups only

The OCF only performs virtual hosting for OCF group accounts.

Each group account may have one virtual host. Requests for an exception to this
rule must be approved by the OCF Board of Directors.

#### Limitations on non-berkeley.edu

The OCF may also host non-berkeley.edu domains. The process is more complicated
in this case. Permission will be granted only for group accounts that can
demonstrate a unique need for having a web site outside of the berkeley.edu
domain. For such domains, the group account must:

 1.   Apply to the OCF Board of Directors for a permission to host this domain.
 2.   Pay any and all fees and/or obtain permissions relating to obtaining and
      maintaining a domain name.

#### University policies

Virtual web sites, just like other OCF user accounts, must comply with the
relevant UC Berkeley [computer use policy][computer-use] and [DNS
policy][dns-policy]. The LEAD Center's [Student Org Domain Name
Guidelines][rso-domains] presents the most relevant information to student
groups.

[computer-use]: https://security.berkeley.edu/policy/usepolicy.html
[dns-policy]: https://security.berkeley.edu/policy/dns
[rso-domains]: http://lead.berkeley.edu/wp-content/uploads/2014/12/student-org-domain-guidelines.pdf

In particular,

* **No off-site (third-party) hosting**: Circumventions around off-site
  hosting, including (but not limited to) proxies, redirects, and substantial
  inline frames (iframes) of non-berkeley.edu domains are not allowed. The OCF
  does not process nor advise off-site hosting requests, which can be
  [submitted directly to the university][offsite] (however, feel free to keep
  us informed if you have an existing OCF account).

  In other words, to comply with university policy, the OCF will only provide
  virtual hosting for websites that are substantially hosted on OCF servers.

[offsite]: https://offsitehosting.berkeley.edu/

#### Hosting badge

All virtual hosts on the OCF must include an [[OCF banner|doc
services/vhost/badges]] on the front page that links to the [[OCF home
page|home]]. The banner need not be displayed extremely prominently, but it
must be noticeable without undue effort. If the banner is removed or misplaced,
the OCF reserves the right to terminate the virtual hosting service. The
hosting badge not only attributes the OCF but also distinguishes it from sites
hosted by University departments.

## Email Forwarding    {email}

Want to send and receive email from `@mygroup.berkeley.edu` addresses? You can
do that!

We call this *mail virtual hosting*. To learn more, [[check out our page about
that|doc services/vhost/mail]].
