[[!meta title="Bootstrapping new desktops"]]

In addition to the [[normal steps for bringing up new machines|help staff/procedures/new-server]],
desktops require a couple extra steps.

## Generate labstats key/cert

[labstats](https://github.com/ocf/labstats) uses HTTPS client auth to
authenticate requests. You need to generate a key/cert for the new computer.

The CA lives on dementors, so that's where you'll make the key and sign it.

    # generate key/cert
    ssh stats
    cd /etc/ssl/stats/ca
    sudo ./create-cert.sh whatever.ocf.berkeley.edu
    scp certs/whatever.ocf.berkeley.edu/whatever.ocf.berkeley.edu.{key,crt} lightning:/tmp/

    # move key/cert to proper path to be provided by puppet
    ssh lightning
    sudo mkdir /opt/puppet/shares/private/whatever/stats
    sudo mv /tmp/whatever.ocf.berkeley.edu.{key,crt} /opt/puppet/shares/private/whatever/stats/
    sudo chown -R puppet:puppet /opt/puppet/shares/private/whatever/

A potential future improvement would be to use some kind of authentication
based on the Kerberos host keys so we don't have to generate extra keys/certs
for every desktop.
