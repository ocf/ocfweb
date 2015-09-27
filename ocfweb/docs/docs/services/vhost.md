[[!meta title="Virtual hosting (group.berkeley.edu)"]]


Virtual hosting allows group accounts to have their website available on a
different domain, typically under berkeley.edu. For example, a group's site can
be made available at `yourgroup.berkeley.edu` in addition to the standard
address under `ocf.berkeley.edu`.

OCF provides two separate (but related) virtual hosting services:

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

1.   [[Request an OCF group account|doc membership]] (if you haven't already done so).
2.   Set up your webspace and upload your website (if you haven't already done so). The website should be developed already, not a placeholder.
3.   Place a [Hosted by OCF banner](https://www.ocf.berkeley.edu/images/hosted-logos/) on your home page that links to the OCF front page. If none of these images are appropriate for your site, you may design one of your own and [[submit it|doc contact]] for approval.
4.   Place the university-mandated student group disclaimer on each page of your website (see the section below).
5. Complete the [virtual hosting request
   form](https://accounts.ocf.berkeley.edu/request-vhost) online.
   OCF staff will review your request and contact the university hostmaster on your
   behalf.

### Including the OCF banner

To place any of the [Hosted by OCF banners](https://www.ocf.berkeley.edu/images/hosted-logos/) on your site, you can use HTML code such as the following:

    <a href="https://www.ocf.berkeley.edu/">
    <img src="https://www.ocf.berkeley.edu/images/hosted-logos/ocfbadge_mini8.png" alt="Hosted by the OCF" width="98" height="39" style="border:0" />
    </a>

The banner is required to be placed only on the home page of your site. You can also create your own OCF banner with approval from the OCF (see instructions above).

### Including the University Student Group Disclaimer    {disclaimer}

The university requires that all student group websites on a subdomain of berkeley.edu contain the following text on each page:

> We are a student group acting independently of the University of
> California. We take full responsibility for our organization and
> this web site.

### Policies

#### Groups only

The OCF only performs virtual hosting for OCF group accounts.

Each group account may have one virtual host. Requests for an exception to this rule must be approved by the OCF Board of Directors.

#### Limitations on non-berkeley.edu

The OCF may also host non-berkeley.edu domains. The process is more complicated in this case. Permission will be granted only for group accounts that can demonstrate a unique need for having a web site outside of the berkeley.edu domain. For such domains, the group account must:

 1.   Apply to the OCF Board of Directors for a permission to host this domain.
 2.   Pay any and all fees and/or obtain permissions relating to obtaining and maintaining a domain name.

#### University policies

Virtual web sites, just like other OCF user accounts, must comply with the relevant UC Berkeley [computer use policy](https://security.berkeley.edu/policy/usepolicy.html) and [DNS policy](https://security.berkeley.edu/policy/dns).

In particular,

* **No off-site (third-party) hosting**: Circumventions around off-site hosting, including (but not limited to) proxies, redirects, and substantial inline frames (iframes) of non-berkeley.edu domains are not allowed. OCF does not process or advise off-site hosting requests, which can be [submitted directly to the university](https://offsitehosting.berkeley.edu/) (however, feel free to keep us informed if you have an existing OCF account).

  In other words, to comply with university policy, OCF will only provide virtual hosting for websites that are substantially hosted on OCF servers.

#### Hosting badge

All virtual hosts on the OCF must include an [OCF banner](https://www.ocf.berkeley.edu/images/hosted-logos/) on the front page that links to the [[OCF home page|home]]. The banner need not be displayed extremely prominently, but it must be noticeable without undue effort. If the banner is removed or misplaced, the OCF reserves the right to terminate the virtual hosting service. The hosting badge not only attributes the OCF but also distinguishes it from sites hosted by other University departments.

## Email Forwarding    {email}

By default, email forwarding is not provided for virtually-hosted group
accounts. Groups can request this service, but should be prepared to deal with an
increase in email spam as a result.

To request email forwarding, email `hostmaster@ocf.berkeley.edu`.

### Configuring Forwarding Addresses

In order to tell the mail server where to forward mail, you must create
`.forward` files (note the leading dot). These files contain a list of email
addresses to forward mail to, specified one per line.

The easiest way to create forward files is to log in via
[[SSH|doc services/shell]]. Once logged in, you can create the files by executing a
command like:

    echo "my_email@example.com" > ~/.forward+officer

This command will create a text file called `.forward+officer` in your home directory which contains only the line `my_email@example.com`. This will forward email going to the new address `officer@group.berkeley.edu` to the existing email address `my_email@example.com`. You should substitute your real email for `my_email@example.com` and whatever group-related email address you'd like to use for the `officer` in `.forward+officer`.

You can create as many of these files as you like. Each file should be named `.forward+name` where `name` is the part before the `@` sign in the new address you want (i.e., `name@group.berkeley.edu`).
