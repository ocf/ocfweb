[[!meta title="Setting up bridging and link aggregation"]]

Bridging and LACP will be configured through puppet, but these
intructions should serve as background and to help debug. A
[bridge][linux-wiki-bridge] is basically an in-kernel network switch,
allowing multiple virtual interfaces to communicate with one another
at layer 2. LACP, or [interface bonding][linux-wiki-bonding], is a
protocol that allows the bandwidth of multiple interfaces to be
aggregated together and treated as a single interface.  The type of
bonding we use, 802.3ad, specifies that the bandwidth of the bonded
interface will be the sum of the bandwidth of each child interface,
while providing fault-tolerance in case a particular sub interface
goes down.

## /etc/network/interfaces

On Debian we can configure the network interfaces to come up at boot by adding
stanzas to `/etc/network/interfaces` or `/etc/network/interfaces.d/<iface>`.

### Bonding

We use bond-mode 4, or 802.3ad. Other types are available, like active-fallback or load balancing,
but we use 802.3ad. Link aggregation needs to be configured on the switch as well to work. Instructions
for doing so can be found in the [[documentation for the switch| doc staff/backend/switch]].

Configuring the bonding interface is relatively simple. One must first install `ifenslave`, and
identify the physical interfaces that will be slaved to the bond virtual interface. Then, write
the following to the config file:

```
auto bond0

iface bond0 inet manual
    slaves <iface> <iface> ...
    bond-mode 802.3ad
    bond-miimon 100
    bond-lacp-rate 1
```

What do these options mean? The first line indicates the interfaces that are going to participate
in the bond. The corresponding ports on the switch are the ones that are going to be aggregated
into a channel-group/port-channel. The second line configures the type of aggregation, 802.3ad
in our case, while the third configures the frequency in miliseconds that the interfaces are
inspected for link failure and the fourth indicates the rate at which LACP PDUs are sent, 1
implying "fast", at a PDU sent every second instead of every 30 seconds ("slow").

If the bond interface is going to be the primary interface on the host, you may want to change
`manual` to `static` and add addressing information by adding `address`, `gateway`, and `netmask`
fields to the stanza. If the bond interface is going to be part of a bridge, leave it as `manual`.


### Bridging

Write the following stanzas to the config file. If using a bridge it's likely you want
the bridge to expose the addressing information for the host.

```
auto br0

iface br0 inet static
    bridge_ports bond0
    bridge_stp off
    bridge_maxwait 0
    address 169.229.226.x
    netmask 255.255.255.0
    gateway 169.229.226.1

iface br0 inet6 static
    address 2607:f140:8801::1:x
    netmask 64
    gateway 2607:f140:8801::1
```

## Configuring interfaces by hand

Much configuration can be done by hand by using the `ip` command. This is useful
for debugging and initial configuration but does not survive reboots.

### Create a bonding interface

```
$ ip link add bond0 type bond mode 4 miimon 100
```

### Bind physical interfaces to the bond interface

```
$ ip link set <iface> master bond0
```

### Show bound interfaces

```
$ ip link show type bond_slave
```

[linux-wiki-bonding]: https://wiki.linuxfoundation.org/networking/bonding
[linux-wiki-bridge]: https://wiki.linuxfoundation.org/networking/bridge
