[[!meta title="Firewall"]]

We use a Cisco ASA firewall provided by IST. We have two cables in our server
room: one behind the firewall, and one not.

See the [pretty good
presentation](https://www.ocf.berkeley.edu/~staff/bod/2014/Fall/2014-09-22.pdf)
from Fall 2014 about our networking.


## Administering to the firewall
### Option 1: Over SSH

To connect, use `ssh -4 you@firewall`. Use your **CalNet ID and password**
(you'll need to get permission if you haven't already).

Some handy commands (first run `enable` and enter your password again):

* Show the running config: `show running-config`

* Enter config options: `configure terminal`

* Save the running config: `copy running-config startup-config`

  (always do this after testing your changes, or they'll revert upon restart!)


### Option 2: Using the Java GUI

This works best on-site, though it sometimes works using X forwarding as well.

We have a handy script which handles downloading a recent Java and starting the
app, located `/opt/share/utils/sbin/firewall`. It should be sufficient to just
launch this script.
