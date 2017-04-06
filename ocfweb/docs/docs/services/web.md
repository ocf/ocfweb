[[!meta title="Web hosting"]]


All OCF accounts include web hosting with an address at:

* **`https://www.ocf.berkeley.edu/~user`** (canonical version)
* **`https://ocf.io/user`** (shorter version)

where `user` is the account name.

Group accounts may also request a [[virtual host|doc services/vhost]] for
another domain (e.g., group.berkeley.edu).

#### Off-site hosting

One question that often comes up is if the OCF is able to host websites
from services such as Squarespace, Wix, Weebly, Tumblr, etc. Unfortunately
due to logistical considerations and University policy, the OCF is unable
to do so. More specifically, the OCF cannot point  <group>.berkeley.edu
domain names to off-campus hosting providers, but it can, however, host
websites exported from such providers.

Many website building services like Wix and Weebly make their money by
using a proprietary service to allow users to design their websites, and
subsequently charge users to host those sites. This means providing the
servers, storage space, internet connection, and configurations to allow
these sites to show up on the internet. Obviously, the OCF is unable to
access this proprietary software and is therefore unable to host sites
developed using them. However, the OCF is capable of hosting anything made
using the free and open-source backends we support, including Wordpress,
Django, Ruby on Rails, Node.js, PHP, and others. You may wish to consider
building your website with those if you desire to host with the OCF.

Furthermore, University policy prohibits campus DNS from redirection to
off-site hosts without explicit permission from the University. This means
that, if you want to host your website with Wix or some other provider, we
cannot give you a URL like group.berkeley.edu that points to that website.
If you would like to host off-site, OCF is not the appropriate point of
contact in such cases - one would have to
[contact the university](https://offsitehosting.berkeley.edu/) directly
to request permission. This is primarily relevant to student groups.

Similarly, the OCF does not generally allow hosting under custom domain names
for student groups. This means we do not usually support things like
"you_or_your_group.com" pointing to a website whose files are hosted on OCF
servers. However, we may agree to host websites under custom domains on a
case-by-case basis, usually for University affiliates such as faculty members,
ASUC/University programs, and others. Please [[contact us|doc contact]] for
more information.

For reference, a typical web hosting scenario involves two things: the domain
name, and the hosting server. The domain name is purchased from a registrar,
and using it involves setting Domain Name System (DNS) records to point to
the address of a hosting server. This server is purchased from any variety
of sources, and must be configured to respond to web requests to the domain
name in question. While the OCF provides both, only a limited subset of their
functionality are available for general use by the campus community due to the
legal, technical, and policy considerations explained above.

## Uploading Files

Upload files to your web space the same way you [[upload files to your OCF
account|doc services/shell]] (typically SFTP if used remotely). The only
difference is that files for your web space are placed in your `public_html`
directory.

## Additional details

The web server runs Apache 2.4 with FastCGI (mod_fcgid), suEXEC, and suPHP.
Access and error logs are accessible in `/opt/httpd` using [[SSH|doc
services/shell]].

The web server itself runs as a dedicated user. If your .htaccess file is not
world-readable (e.g., `chmod 644`), the web server will return the error "401
Forbidden".

PHP/CGI/FastCGI scripts are executed as your user, so they do not need to be
world-readable. If they contain sensitive information (such as database
passwords), you should make them private (e.g., `chmod 600` or `chmod 700`).

Both individual hosting and student group hosting are done entirely over HTTPS.


### Supported languages

* PHP 5.6
* Perl 5.20.2
* Python 2.7, and 3.4; Django 1.7.7; Flask 0.10.1
* Ruby 2.1.5; Rails 4.1.8

Other flavors of the day may work but are not currently supported. We may be
able to install additional packages on request, but will generally advise you
to use alternatives instead (such as installing in a virtualenv or inside your
home directory).


## FAQ

### My `public_html` directory is missing, how do I fix that?

We automatically create the `public_html` symlink for all new accounts, but
it's possible that it was accidentally removed (or that you have an older
account from before we started the practice).

Keep in mind that just recreating the directory is *not* sufficient; it must be
a symbolic link to your actual web space. If you simply make a directory named
`public_html`, it won't be used for your website.

Here are two easy ways to re-create the symlink:


#### via the web interface

1. Open the [[web commands interface|commands]] in your web browser.
2. Select the "makehttp" option. Enter your OCF username and password, and
   choose "Run command". You should see something like this in the output,
   assuming you entered your username and password correctly:

        public_html folder has been created successfully.


#### via SSH

1. Login to your account via [[SSH|doc services/shell]].
2. After you go past all system messages, you will see prompt:

        tsunami$

    At this prompt, type `makehttp`. This command will create your web
    directory. Here's a sample screen output:

        tsunami$ makehttp
        public_html folder has been created successfully.
