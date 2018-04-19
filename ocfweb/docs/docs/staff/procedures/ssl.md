[[!meta title="SSL certificates"]]

We are able to obtain signed certificates at no charge through the campus
[InCommon-Comodo certificate
service](https://calnetweb.berkeley.edu/calnet-technologists/calnet-incommon-comodo-certificate-service).

The primary Common Name for a certificate should always be the **server
hostname**, with service CNAMEs specified as Subject Alternative Names. A
certificate for our apt repository/mirrors should have the primary CN
`fallingrocks.ocf.berkeley.edu`, with `apt.ocf.berkeley.edu`
and `mirrors.ocf.berkeley.edu` as SANs.

This allows us to easily distinguish between certificates in cases where a
service may be hosted by multiple hostnames, or where the hostname changes,
without sharing private keys.

## Setting up SSL

### Generating a key/CSR

The easiest way to generate a key and CSR is with the `makessl` script provided
by `ocf/utils`. Specify the fully-qualified hostname of the server as the only
argument. **Do not use service CNAMEs.**

Example usage:

    /opt/share/utils/staff/ssl/makessl supernova.ocf.berkeley.edu

This will create a file `supernova.ocf.berkeley.edu.key` in the same directory,
and print a CSR to stdout.

### Requesting a Certificate

1. Go to the [InCommon Certificate
   Manager](https://cert-manager.com/customer/incommon) (or have the current
   Departmental Certificate Administrator go there).

2. Click "Add" to request a new certificate.

3. Select the type of certificate (either "InCommon SSL" or "InCommon
   Multi-Domain SSL" if you need SANs), paste the CSR, and hit OK.

5. Approve the certificate and wait for it to be issued. Download "X509
   Certificate Only" and place it in a file named `${fqdn}.crt` in the same
   directory as the key.

### Installing key/certificate with Puppet

You should install the key and certificate via Puppet. On lightning, create the
directory `/opt/puppet/shares/private/$fqdn/ssl` and place the key and cert in
it.

Add the `ocf_ssl` module to the server (e.g. by adding it to the server's
hiera config). This will provide the files:

* `/etc/ssl/private/${fqdn}.key`
* `/etc/ssl/private/${fqdn}.crt`
* `/etc/ssl/private/${fqdn}.bundle`

The bundle file is automatically generated from the certificate you provided,
and contains the InCommon intermediate certificate.


## Verifying certificates

For the host `rt.ocf.berkeley.edu` on port 443 (HTTPS), try connecting using
the OpenSSL client.

    openssl s_client -CApath /etc/ssl/certs -connect rt.ocf.berkeley.edu:443

The last line of the SSL session information should have a zero return code.
This only verifies the certificate, not that the hostname you entered matches
the Common Name or Subject Alternatives Names on the certificate.

Good:

    Verify return code: 0 (ok)

Bad example 1:

    Verify return code: 18 (self signed certificate)

The default self-signed certificate, not the one obtained through InCommon, is
probably still being used.

Bad example 2:

    Verify return code: 21 (unable to verify the first certificate)

The intermediate CA chain is probably missing (or in the wrong order), so there
is no trust path to a root CA.
