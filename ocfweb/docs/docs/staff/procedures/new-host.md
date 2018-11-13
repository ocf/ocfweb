[[!meta title="Creating new hosts (servers, desktops)"]]

Bringing up new hosts is pretty easy, but has a few easy-to-miss steps. This
process requires both root and a `/admin` principal.

It's preferable to not bring up servers at a whim, but if you must, you should
use hostnames of the form `hozer-{60..89}` and their corresponding IP addresses
(rather than allocating new ones). Please clean up when you're finished by
running `virsh undefine hozer-{num}` to remove the VM and `lvremove
/dev/vg/hozer-{num}` to remove the logical volume.


## Step 0. Pick a hostname and IP

If you are creating a brand-new host, you can find a list of IP addresses
already in use in our [DNS repo on GitHub][github-ip-list]. Hostnames must be
based on (un)natural disasters; check out `~staff/server_name_ideas` if you're
having trouble thinking of one.

[github-ip-list]: https://github.com/ocf/dns/blob/master/etc/zones/db.226.229.169.in-addr.arpa


## Step 1. (New hosts only) Add to LDAP, DNS, Puppet, Kerberos

Only do these if a server with this hostname has never existed before (or if
it's been long enough that some of these steps have never been done before).
Unfortunately, these steps tend to change a lot as our infrastructure evolves.


### Step 1.1. Add the LDAP entry

On supernova, `kinit $USER/admin ldap-add-host <hostname> <ip>`. If setting up
a desktop, also do `kinit $USER/admin ldapvi cn=<hostname>` and set the `type`
attribute to `desktop`. If doing a staff VM, set it to `staffvm` instead.


### Step 1.2. Add the DNS record

Clone the [DNS repo][github-dns] from GitHub, run `make`, and push a commit
with the new records.

[github-dns]: https://github.com/ocf/dns


### Step 1.3. Add node config to Puppet

Only do this if you are creating a staff VM, a server which will run a service,
or a special snowflake. Make a commit to the [Puppet repo][github-puppet] which
adds a file `hieradata/nodes/<hostname>.yaml` for the new host. Follow the
example of a similar node's `host.yaml` file.

[github-puppet]: https://github.com/ocf/puppet


### Step 1.4. Create the Kerberos keytab

On the puppetmaster, run `sudo gen-keytab`.


## Step 2. Create the host, run Debian installer


### Virtual hosts

We have a handy script, `makevm`, that:

* Creates a logical volume (disk) for the new VM
* Adds a new VM using virt-install and PXE boots it
* Waits for the Debian installer to finish
* SSHs to the new server and sets its IP

To use it, log on to the target physical server (`riptide`, `hal`, `pandemic`, or `jaws`),
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


## Step 3. Log in and start Puppet

### Virtual hosts

The `makevm` script at the very end drops you into a shell. In this shell, you
should run:

1. `puppet agent --test`.


### Physical hosts

1. Log in as `root:r00tme`. You can change the password if you want, but don't
   have to (Puppet will change it soon anyway).
2. Make sure the IP address and hostname is set correctly. This may have
   happened by DHCP if it's a desktop, but if not, fix it and restart:

   1. Edit `/etc/hostname` so it has the desired hostname instead of
      dhcp-_whatever_.
   2. Run `hostname -F /etc/hostname`.
   3. Find out what the ethernet interface's name and current IP address is
      by running `ip addr`. The ethernet interface should be named something
      like `eno1` or `enp4s2`. (In the following instructions, substitute
      `eno1` with the correct name.)
   4. Remove the incorrect IP addresses with `ip addr del $WRONG_ADDRESS
      dev eno1`.
   5. Add the correct IP addresses with `ip addr add $CORRECT_ADDRESS
      dev eno1`. Make sure that $CORRECT_ADDRESS includes the netmask.

3. `puppet agent --test`


## Step 4. Sign the Puppet cert and run Puppet

On the puppetmaster, `sudo puppetserver ca list` to see pending requests. When
you see yours, use `sudo puppetserver ca sign --certname hostname.ocf.berkeley.edu`.

Log back into the host and run `puppet agent --test` to start the Puppet
run. You may need to repeat this once or twice until the run converges.


### Step 4.1. Upgrade packages

The first Puppet run and various other things may be broken if one or more
packages are out of date, e.g. Puppet. Remedy this with an `apt update &&
apt upgrade`.
