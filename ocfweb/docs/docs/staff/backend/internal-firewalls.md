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

 * All servers allow traffic from internal servers, which are considered
   trusted. For instance, all servers will accept traffic from supernova.
 * All servers disallow traffic from the DMZ by default, as those hosts are
   considered untrusted. For instance, hal will not accept traffic from tsunami
   without a special exception. (DMZ servers can't even talk to other DMZ
   servers by default.)
 * Some servers allow certain traffic from DMZ servers. The precise rules can be
   found in the puppet code. Generally:
    * DMZ servers can talk to needed production services on the appropriate
      ports.
    * Staff VMs allow all incoming traffic.
    * Staff VMs and desktops are allowed to directly SSH into internal servers.
    * There are other miscellaneous rules allowing other traffic.

In addition to input rules, it's necessary to have some output rules as well to
protect devices that we don't trust to have reliable firewalls, such as printers
and IPMI devices. The rules for those devices work a little differently:

 * A handful of "uber-trusted" servers, such as supernova and hypervisors, are
   allowed to talk to all of these special devices. This allows us to use these
   servers for the purposes of configuring or debugging those devices.
 * Some other servers can talk to certain special devices. For example, the
   print server can talk to printers.
 * Most other hosts cannot talk to these special devices.

Output rules are not a perfect solution, since they operate on a voluntary
mechanism and can't prevent non-OCF hosts that may be connected to our network
from contacting these special devices anyway. Preventing this is a future
project.

It's important to note that internal firewalls are set up to only filter traffic
from other OCF machines. Traffic from outside the OCF network is the sole
responsibility of the external firewall.

[dmz]: https://en.wikipedia.org/wiki/DMZ_(computing)


## Implementation

Internal firewalls are implemented using iptables rules set by Puppet with the
[puppetlabs-firewall module][puppetlabs-firewall]. We place all of our input
rules in the `PUPPET-INPUT` chain and all of our output rules in the
`PUPPET-OUTPUT` chain.

Firewall rules are added by using `firewall_multi` and
`ocf::firewall::firewall46` declarations:
 * `ocf::firewall::firewall46` should generally be used in most cases. It
   inserts IPv4 and IPv6 iptables rules, but only adds the IPv6 iptables rule if
   the host has a public IPv6 address. This prevents Puppet errors otherwise
   occurring due to IPv6 addresses not being resolved.
 * `firewall_multi` should be used if IP addresses need to be manually specified
   in the firewall rule.
 * `ocf::firewall::firewall46` and `firewall_multi` both internally use the
   `firewall` resource. Direct use of the `firewall` resource should be avoided
   since such resources wouldn't be subject to the [ordering constraints
   generally placed on firewall resources][ordering].

[ordering]: https://github.com/ocf/puppet/blob/f3fdd5912a5dc5eafd9995412a9c5e85874dee31/manifests/site.pp#L50-L58
[puppetlabs-firewall]: https://forge.puppet.com/puppetlabs/firewall


## Debugging

### `iptables` commands

Note that all of the following commands need to be run as root.

The `iptables` command allows you to inspect and debug IPv4 firewall rules:

 * `iptables -L`: list firewall rules
    * `iptables -L PUPPET-INPUT` lists our input firewall rules
    * `iptables -L PUPPET-OUTPUT` lists our output firewall rules
    * You can add a `-v` option to list more detailed info (like statistics and
      input/output interface)
    * You can add a `-n` option to show IP addresses and port numbers instead of
      hostnames and port names
 * `iptables -F <chain>`: deletes all of the rules in the given chain.
    * It seems that in some circumstances iptables may be buggy and not remove a
      rule that Puppet tells it to remove. This seems to be more likely to occur
      when the rule is the only rule in its chain. In this case, running
      `iptables -F` on that chain and subsequently rerunning Puppet will clear
      the issue.
 * `iptables -D <chain> <rulenum>`: Deletes the _rulenum_-th rule from the given
   chain (i.e. `PUPPET-INPUT` or `PUPPET-OUTPUT`).
 * `iptables -A <chain> <rule-specification>`: Adds the specified rule to the
   given chain. Note that this command is not particularly useful for the
   `PUPPET-INPUT` and `PUPPET-OUTPUT` chains, since any added rules will be
   purged by Puppet.

For IPv6 firewall rules, you need to use the `ip6tables` command instead. The
invocation is the same as for `iptables`.

Iptables rules are not automatically persisted across reboots. In order for your
changes to iptables to be preserved across reboots, you need to additionally
run `service netfilter-persistent save`. This is done automatically after
every Puppet run which results in iptables rules being modified, but if you
manually fiddle with iptables you may need to run it yourself.

### Disabling firewalls through hiera

In an emergency, it's possible to effectively disable firewalling of input
traffic on a server by setting `ocf::firewall::reject_unrecognized_input` to
`false` in that server's hieradata. Turning on this option causes the rules in
the PUPPET-INPUT chain which reject traffic to be deleted, effectively disabling
the firewall's function of filtering input packets.

An analogous kill switch does not currently exist for output-traffic
firewalling, but can be easily added.
