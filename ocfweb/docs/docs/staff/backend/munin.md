[[!meta title="Munin"]]

We use [Munin](https://munin.ocf.berkeley.edu) to provide real-time monitoring
of our hardware. The master is [[dementors|doc staff/backend/servers]] which
runs a cron job every five minutes to collect data from the node server running
on each machine. A [custom script][gen-munin-nodes] periodically generates the
list of available nodes from LDAP.

We monitor servers, desktops, and staff VMs, but not the hozer boxes.
Additionally, we don't receive email alerts for staff VMs.

## Automated alerts

Munin sends mail to root whenever certain stats run out of bounds for a
machine, e.g. if disk usage goes above 92%. Some plugins have configurable
warning and critical levels for each field, which are usually set in the node
config like so:

```text
[pluginname]
env.fieldname_warning min:max
env.fieldname_critical min:max
```

The warning bounds for each node are generated from a Puppet template in the
`ocf` module using machine specs from facter. While config files use
underscores, the display name for a variable's warning levels takes the form
`fieldname.warning` or `fieldname.critical`.

When `munin-limits` finds a variable in warning or critical range, it pipes the
alert text to [another script][mail-munin-alert] which filters out
uninteresting or noisy messages and emails the rest to root. Munin itself isn't
very flexible about disabling alerts from plugins, so, if there is a noisy
variable you want to ignore alerts for, you can add it to the list of
`IGNORED_WARNINGS`.

## Custom plugins

We provide a Puppet class, `ocf::munin::plugin`, which installs a custom Munin
plugin to a machine, for example, to monitor the number of players on our CS:GO
server. Writing a plugin is very easy, should you need to do so. When called
without arguments, it should print to standard output a list of variable names
and values:

```text
field1.value <value>
field2.value <value>
...
```

When given the lone argument `config`, it should print display information for
Munin graphs and variable warning levels:

```text
graph_title Title
graph_vlabel yaxis
graph_scale no
field1.label label
field1.warning min:max
...
```

[gen-munin-nodes]: https://github.com/ocf/puppet/blob/master/modules/ocf_stats/files/munin/gen-munin-nodes
[mail-munin-alert]: https://github.com/ocf/puppet/blob/master/modules/ocf_stats/files/munin/mail-munin-alert
[ocf_munin_plugin]: https://github.com/ocf/puppet/blob/master/modules/ocf/manifests/munin/plugin.pp
