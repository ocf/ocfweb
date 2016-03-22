[[!meta title="Firewall"]]

We use a Cisco ASA firewall provided by IST. We have one network port in the
server room which is activated and behind the firewall; we have another network
port activated in the lab behind the television which is also behind the
firewall.


## Administering to the firewall
### Option 1: Over SSH

To connect, use `ssh -4 you@firewall`. Use your **CalNet ID and password**
(you'll need to get permission if you haven't already).

Some handy commands (first run `enable` and enter your password again):

* Show the running config: `show running-config`

* Enter config options: `configure terminal`

* Save the running config: `copy running-config startup-config`

  (always do this after testing your changes, or they'll revert upon restart!)

(These commands are similar to the commands used for the
[[switch|help staff/backend/switch]].)


### Option 2: Using the Java GUI

This works best on-site, though it sometimes works using X forwarding as well.

We have a handy script which handles downloading a recent Java and starting the
app, located `/opt/share/utils/sbin/firewall`. It should be sufficient to just
launch this script.


## Automatic config diffs

IST has configured [rancid](http://www.shrubbery.net/rancid/) to both back up
and send us email diffs of the firewall's config.
