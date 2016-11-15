[[!meta title="Creating new hosts (servers, desktops)"]]

Bringing up new hosts is pretty easy, but has a few easy-to-miss steps. This
process requires both root and a `/admin` principal.

It's preferable to not bring up servers at a whim, but if you must, you should
use hostnames of the form `hozer-{60..89}` and their corresponding IP addresses
(rather than allocating new ones). Please clean up when you're finished by
running `virsh undefine hozer-{num}` to remove the VM and `lvremove
/dev/vg/hozer-{num}` to remove the logical volume.

## Step 1. Pick a hostname and IP

Add the hostname to the DNS. Contact the University hostmaster to request the
reverse DNS record.


## Step 2. Create the host, run Debian installer

### Virtual hosts

We have a handy script, `makevm`, that:

* Creates a logical volume (disk) for the new VM
* Adds a new VM using virt-install and PXE boots it
* Waits for the Debian installer to finish
* SSHs to the new server and sets its IP

To use it, log on to the target physical server (`hal`, `pandemic`, or `jaws`),
and run `makevm --help`. A typical invocation looks something like:

    makevm -m 4096 -c 2 -s 15 arsenic 169.229.226.47


### Physical hosts

All you need to do to run the Debian installer is PXE boot. On desktops, you
sometimes need to enable this in the BIOS before you can select it from the
boot menu.

Be warned that the default action (automated install) happens after 5 seconds.
So don't PXE-boot your laptop and walk away!

We preseed a bunch of settings (random questions, mirror locations, packages,
etc.). The install should be completely hands-free, and will restart to a login
tty.


## Step 3. Log in and run Puppet

### Virtual hosts

1. Log in as `root:r00tme`
2. `puppet agent --enable`.

### Physical hosts

1. Log in as `root:r00tme`. You can change the password if you want, but don't
   have to (Puppet will change it soon anyway).
2. Make sure the IP address and hostname is set correctly. This probably
   happened by DHCP if it's a desktop, but if not, fix it and restart.
3. Make sure you you don't have duplicate entries in
   `/etc/udev/rules.d/70-persistent-net.rules` for `eth0` and `eth1` (see
   rt#3050). If you do, remove `eth1` and restart.
4. `puppet agent --enable`
5. `puppet agent --debug --no-daemonize`.


## Step 4. Create Kerberos keytab and LDAP entry

Only do these if a server with this hostname has never existed before.

1. On supernova, `kinit $USER/admin ldap-add-host <hostname> <ip>`.
2. On the puppetmaster, run `/opt/puppet/scripts/gen-keytab`


## Step 5. Sign the Puppet cert and run Puppet

On the puppetmaster, `puppet ca list` to see pending requests. When you see
yours, use `puppet ca sign hostname.ocf.berkeley.edu`.

Log back into the host and do `systemctl restart puppet` to start the Puppet
run. Monitor the run with `journalctl -f`. Restart Puppet once or twice more
until the configuration converges.
