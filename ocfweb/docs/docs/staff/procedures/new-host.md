[[!meta title="Creating new hosts (servers, desktops)"]]

Bringing up new hosts is pretty easy, but has a few easy-to-miss steps. This
process requires both root and a `/admin` principal.

It's preferable to not bring up servers at a whim, but if you must, you should
use hostnames of the form `hozer-{60..89}` and their corresponding IP addresses
(rather than allocating new ones). Please clean up when you're finished by
running `virsh undefine hozer-{num}` to remove the VM and `lvremove
/dev/vg/hozer-{num}` to remove the logical volume.


## Step 0. Pick a hostname and IP    {pick-hostname}

If you are creating a brand-new host, you can find a list of IP addresses
already in use in our [DNS repo on GitHub][github-ip-list]. Hostnames must be
based on (un)natural disasters; a few previously used ones may be listed at the
bottom of [our DNS template][github-dns-template].

[github-ip-list]: https://github.com/ocf/dns/blob/master/etc/zones/db.ocf.in-addr.arpa
[github-dns-template]: https://github.com/ocf/dns/blob/master/templates/db.ocf.tmpl


## Step 1. (New hosts only) Add to LDAP, DNS, Puppet, Kerberos

Only do these if a server with this hostname has never existed before (or if
it's been long enough that some of these steps have never been done before).
Unfortunately, these steps tend to change a lot as our infrastructure evolves.


### Step 1.1. Add the LDAP entry    {add-ldap}

On supernova, `kinit $USER/admin ldap-add-host <hostname> <ip>`. If setting up
a desktop, also do `kinit $USER/admin ldapvi cn=<hostname>` and set the `type`
attribute to `desktop`. If doing a staff VM, set it to `staffvm` instead.


### Step 1.2. Add the DNS record    {add-dns}

Clone the [DNS repo][github-dns] from GitHub, run `make`, and push a commit
with the new records.

[github-dns]: https://github.com/ocf/dns


### Step 1.3. Add node config to Puppet    {add-puppet}

Only do this if you are creating a staff VM, a server which will run a service,
or a special snowflake. Make a commit to the [Puppet repo][github-puppet] which
adds a file `hieradata/nodes/<hostname>.yaml` for the new host. Follow the
example of a similar node's `host.yaml` file.

[github-puppet]: https://github.com/ocf/puppet


### Step 1.4. Create the Kerberos keytab    {add-kerberos}

On the puppetmaster, run `sudo gen-keytab`.


## Step 2. Create the host, run Debian installer    {debian-installer}


### Virtual hosts    {debian-virtual}

We have a handy script, `makevm`, that:

* Creates a logical volume (disk) for the new VM
* Adds a new VM using virt-install and PXE boots it
* Waits for the Debian installer to finish
* SSHs to the new server and sets its IP

To use it, log on to the target physical server (`hal`, `pandemic`, or `jaws`),
and run `makevm --help`. A typical invocation looks something like:

    makevm -m 4096 -c 2 -s 15 arsenic 169.229.226.47


### Physical hosts    {debian-physical}

All you need to do to run the Debian installer is PXE boot. On desktops, you
sometimes need to enable this in the BIOS before you can select it from the
boot menu.

Be warned that the default action (automated install) happens after 5 seconds.
So don't PXE-boot your laptop and walk away!

We preseed a bunch of settings (random questions, mirror locations, packages,
etc.). The install should be completely hands-free, and will restart to a login
tty.


## Step 3. Log in and start Puppet    {start-puppet}

### Virtual hosts    {puppet-virtual}

1. Log in as `root:r00tme`
2. `puppet agent --enable`.


### Physical hosts    {puppet-physical}

1. Log in as `root:r00tme`. You can change the password if you want, but don't
   have to (Puppet will change it soon anyway).
2. Make sure the IP address and hostname is set correctly. This probably
   happened by DHCP if it's a desktop, but if not, fix it and restart.
3. Make sure you you don't have duplicate entries in
   `/etc/udev/rules.d/70-persistent-net.rules` for `eth0` and `eth1` (see
   rt#3050). If you do, remove `eth1` and restart.
4. `puppet agent --enable`
5. `puppet agent --debug --no-daemonize`.


## Step 4. Sign the Puppet cert and run Puppet    {puppet-cert}

On the puppetmaster, `sudo puppet ca list` to see pending requests. When you see
yours, use `sudo puppet ca sign hostname.ocf.berkeley.edu`.

Log back into the host and do `systemctl restart puppet` to start the Puppet
run. Monitor the run with `journalctl -f`. Restart Puppet once or twice more
until the configuration converges.


### Step 4.1. Upgrade packages    {upgrade-packages}

The first Puppet run and various other things may be broken if one or more
packages are out of date, e.g. Puppet. Remedy this with an `apt-get update &&
apt-get upgrade`.
