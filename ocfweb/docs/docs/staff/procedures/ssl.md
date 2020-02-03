[[!meta title="SSL certificates"]]

We are able to obtain signed certificates at no charge through [Let's
Encrypt](https://letsencrypt.org/).

The primary Common Name for a certificate should always be the **server
hostname**, with service CNAMEs specified as Subject Alternative Names. For
instance, a certificate for our apt repository/mirrors should have the primary
CN `fallingrocks.ocf.berkeley.edu`, with `apt.ocf.berkeley.edu` and
`mirrors.ocf.berkeley.edu` as SANs.

This allows us to easily distinguish between certificates in cases where a
service may be hosted by multiple hostnames, or where the hostname changes,
without sharing private keys.


## Add relevant entries to LDAP/DNS

The SSL support within Puppet relies on the `dnsA` and `dnsCname` entries for a
host within LDAP. These are also converted in the ocf/dns repo into
BIND-parsable files, so if you update LDAP and then update the ocf/dns repo,
you should be ready to go!


## Setting up SSL with Puppet

Add the `ocf::ssl::default` module to the server (e.g. by adding it to the
server's per-host hiera config). This will run
[`dehydrated`](https://dehydrated.io/) to update DNS dynamically (a dns-01
challenge) and spit out a valid cert. This will automatically retrieve a cert
for a host that matches as much as it can in terms of SANs. For instance, if
requesting for a host with a hostname of `foo` with an alias of `bar`, it will
request `foo.ocf.berkeley.edu`, `bar.ocf.berkeley.edu`, `foo.ocf.io`, and
`bar.ocf.io`. If you need to customize this list, use the `ocf::ssl::bundle`
class and pass in a list of domains.

If puppet successfully runs, it should provide these files for whatever service you
want to setup that needs SSL:

* `/etc/ssl/private/${fqdn}.key`
* `/etc/ssl/private/${fqdn}.crt`
* `/etc/ssl/private/${fqdn}.bundle`

The bundle file is automatically generated from the certificate you provided,
and contains the Let's Encrypt intermediate certificate.

You should also make sure to notify the service automatically so that when any
new certs come along they are automatically used by the service. This requires
linking the `ocf::ssl::default` module with whatever service you're using the
cert within. For instance, to restart nginx when certs are updated, add this
into your puppet manifest:

```puppet
Class['ocf::ssl::default'] ~> Class['Nginx::Service']
```


## Verifying certificates

For the host `rt.ocf.berkeley.edu` on port 443 (HTTPS), try connecting using
the OpenSSL client.

```bash
openssl s_client -CApath /etc/ssl/certs -connect rt.ocf.berkeley.edu:443
```

The last line of the SSL session information should have a zero return code.
This only verifies the certificate, not that the hostname you entered matches
the Common Name or Subject Alternatives Names on the certificate.

Good:

    Verify return code: 0 (ok)

Bad example 1:

    Verify return code: 18 (self signed certificate)

The default self-signed certificate, not the one obtained through Let's
Encrypt, is probably still being used.

Bad example 2:

    Verify return code: 21 (unable to verify the first certificate)

The intermediate CA chain is probably missing (or in the wrong order), so there
is no trust path to a root CA.
