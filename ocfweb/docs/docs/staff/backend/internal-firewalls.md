[[!meta title="Internal firewalls"]]

While the [[external firewall|doc staff/backend/firewall]] regulates network
traffic to the OCF from outside the OCF network, internal firewalls are
responsible for regulating network traffic between different machines within the
OCF.

OCF machines are broadly classed into internal and [DMZ][dmz]. Internal machines
are those which are not running user code and are not staff VMs, specifically
those in the IP range 5-90 (excluding the ones in the DMZ listed below). The DMZ
consists of all other machines, including:

 * Those running user code (tsunami, werewolves, death, and desktops)
 * Staff VMs
 * External machines plugged into the OCF network (e.g. staffers' laptops)

Each server filters input traffic as follows:

 * All servers allow traffic from internal servers. For instance, supernova can
   talk to any other server.
 * All servers disallow traffic from the DMZ by default. For instance, tsunami
   cannot talk to hal without a special exception. DMZ servers can't even talk
   to other DMZ servers by default.
 * Some servers allow certain traffic from DMZ servers. The precise rules can be
   found in the puppet code. Generally:
    * DMZ servers can talk to needed production services on the appropriate ports.
    * Staff VMs allow all incoming traffic.
    * Staff VMs and desktops are allowed to directly SSH into internal servers.
    * There are other miscellaneous rules allowing other traffic.

In addition to input rules, it's necessary to have some output rules as well to
protect machines that don't have their own firewalls, such as printers and IPMI
devices. The rules for those machines work a little differently:

 * A handful of "uber-trusted" machines, such as supernova and hypervisors, are
   allowed to talk to all of these special devices.
 * Some other machines can talk to certain special devices. For example, the
   print server can talk to printers
 * Most other machines cannot talk to these special devices.

It's important to note that internal firewalls are set up to only filter traffic
from other OCF machines. Traffic from outside the OCF network is the sole
responsibility of the external firewall.

[dmz]: https://en.wikipedia.org/wiki/DMZ_(computing)

## Implementation

Internal firewalls are implemented using iptables rules set by Puppet with the
[puppetlabs-firewall module][puppetlabs-firewall]. We place all of our input
rules in the `PUPPET-INPUT` chain and all of our output rules in the
`PUPPET-OUTPUT` chain.

[puppetlabs-firewall]: https://forge.puppet.com/puppetlabs/firewall
