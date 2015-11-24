[[!meta title="Managed switch (blackhole)"]]

We use a [Cisco Catalyst 2960S-48TS-L Switch][switch] in our server rack. Each
desktop connects first to the back of a patch panel, and then from a port on
the patch panel to a port on the switch. The servers connect directly to the
switch, as does our uplink to IST.

In its current operation, the switch performs just like an unmanaged switch.
Ideally, we'd eventually like to use some of its more advanced features to do
things like prevent desktops from spoofing servers.

The desktops are connected to ports 1 through 36. The servers are using ports
37 through 47. The IST uplink is port 48.


## Administering the switch over SSH

To connect, use `ssh admin@blackhole`. You can find the password in the list of
admin passwords.

Some handy commands (first run `enable` and enter your password again):

* Show the running config: `show running-config`

* Enter config options: `configure terminal`

* Save the running config: `copy running-config startup-config`

  (always do this after testing your changes, or they'll revert upon restart!)

(These commands are similar to the commands used for the
[[firewall|doc staff/backend/firewall]].)


## Automatic config diffs

We use [rancid](http://www.shrubbery.net/rancid/) to both back up and send us
email diffs of the switch's config.


[switch]: http://www.cisco.com/c/en/us/support/switches/catalyst-2960s-48ts-l-switch/model.html
