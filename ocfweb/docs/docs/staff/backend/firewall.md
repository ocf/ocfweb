[[!meta title="Firewall"]]

We use a [Cisco ASA 5585-X firewall (SSP-20)][asa-5585] provided by IST. We
have one network port in the server room which is activated and behind the
firewall; we have another network port activated in the lab behind the
television which is also behind the firewall. All the ports the desktops use
are also behind the firewall.

[asa-5585]: http://www.cisco.com/c/en/us/products/collateral/security/asa-5500-series-next-generation-firewalls/product_bulletin_c25-614415.html

## Administering the firewall

### Option 1: Over SSH

To connect, use `ssh you@firewall`. Use your **CalNet ID and password** (you'll
need to get permission if you haven't already).

Some handy commands (first run `enable` and enter your password again). Note
that any new config is applied immediately without any need to restart or
reload. However, changes will revert on restart unless they are saved to the
startup config (see below):

* To show a list of available commands, append `?` after the command: For
  example, use `?` by itself to show all possible starts to commands or `show
  ?` to list just the sub-commands under `show`.

* Show the running config: `show running-config`

* Enter config mode (to add or remove options): `configure terminal`

* Add a new object (host/subnet) to the firewall. Must be in config mode before
  using these commands. Replace `host` with the FQDN of the host to add. The
  commands show below are for IPv4 only, replace `host4` with `host6` and `v4`
  with `v6` for IPv6. Using `host4` and `host6` is just a naming convention, it
  is not required, but it makes the config file a lot easier to work with:

      object network host4
        fqdn v4 host.ocf.berkeley.edu

  For example, for IPv6 supernova:

      object network supernova6
        fqdn v6 supernova.ocf.berkeley.edu

  To use both IPv4 and IPv6, an `object-group` definition should to be added to
  group together the two objects for easier further configuration:

      object-group network host
        network-object object host4
        network-object object host6

* To remove a config option, do the same as adding it, but put `no` before the
  definition, so for instance to remove a NTP server added with `ntp server
  169.229.226.12`, remove it with `no ntp server 169.229.226.12`.

* To exit config mode or an object declaration: `exit` (may need to be run
  multiple times to fully exit a config definition).

* Save the running config: `copy running-config startup-config`

  (always do this after testing your changes, or they'll revert upon restart!)

(These commands are similar to the commands used for the [[switch|doc
staff/backend/switch]].)


### Option 2: Using the Java GUI

This works best on-site, though it sometimes works using X forwarding as well.

We have a handy script (just run `firewall`) which handles downloading a recent
Java and starting the app. It should be sufficient to just launch this script.
However, the Cisco cert provided is out of date, so you will likely have to
click through some security warnings to get it to start.


## Automatic config diffs

IST has configured [rancid](http://www.shrubbery.net/rancid/) to both back up
and send us email diffs of the firewall's config, however it has been broken
since 11/21/2016. We also typically get a weekly dump of the entire config over
email (if it wasn't broken currently).
