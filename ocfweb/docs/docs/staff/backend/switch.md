[[!meta title="Managed switches"]]

We use an [Arista 7050SX-64][primary-switch] 10GbE switch as a primary switch
for our servers, and two [Arista 7048T-A][secondary-switch] 1GbE switches for
desktops and management respectively. These devices were donated to us by
Arista Networks in Fall 2018. Each device in the lab connects first to the back
of a patch panel, and then from a port on the patch panel to a port on one of
the 7048T-As via Cat6. The servers connect directly to the 7050SX via SFP+ DACs,
as does our uplink to IST, through a Cat6 to 1GbE SFP+ converter. The 7048T's
connect to the 7050SX through their SFP+ uplink ports.

We do not currently use many of the managed features of the switches, mostly using
them to provide layer 2 connectivity. Our previous switch, a Cisco Catalyst 2960S,
was used for some time to drop [Spanning-tree protocol BPDUs][stp] and [IPv6 Router Advertisements][ipv6-ra]
on all ports, as they caused network configuration problems on our end (creating loops
with IST, or hosts autoconfiguring themselves via SLAAC).

The one advanced feature that we do use on our primary switch is LACP. All of our
hypervisors use Solarflare SFN8522-R2 dual-port 10GbE SFP+ NICs. Both ports are plugged
into the switch, with each hypervisor occupying a vertical pair of switch ports. Each
vertical pair is configured into a channel-group and port-channel, numbered according
to the index of the pair, e.g. ports Ethernet 31 and Ethernet 32 are aggregated into
port-channel 16. The hypervisors are then configured to bond the two interfaces in LACP mode.

In the future, we'd like to make use of some of the more advanced features
available on our switches, such as Port Security, to do things like preventing
desktops from spoofing servers, or using layer 3 functionality to support NAT on
the desktops and other devices.

## Administering the switch

The primary switch is named `blackhole` and can be accessed over SSH from inside
the OCF subnet.

```
$ ssh admin@blackhole.ocf.berkeley.edu
Password:
blackhole.ocf.berkeley.edu>
```

The switches can also be administered directly by connecting to their console port
with a USB serial console cable.

After logging in, one can enter an advanced configuration mode by typing "`enable`",
and then, before configuring specific interfaces, type "`config`".

```
blackhole.ocf.berkeley.edu> enable
blackhole.ocf.berkeley.edu# config
blackhole.ocf.berkeley.edu(config)# interface Ethernet 31-32
blackhole.ocf.berkeley.edu(config-if-Et31-32)#
```

### Configuring LACP

After identifying which interfaces need to be aggregated into an LACP group on the
switch and calculating the group index, enter config mode and do the following:

```
blackhole.ocf.berkeley.edu(config)# interface Ethernet 31-32
blackhole.ocf.berkeley.edu(config-if-Et31-32)# channel-group 16 mode active
blackhole.ocf.berkeley.edu(config-if-Et31-32)# lacp rate fast
blackhole.ocf.berkeley.edu(config-if-Et31-32)# interface port-channel 16
blackhole.ocf.berkeley.edu(config-if-Po16)#
```

at this point, one can use `show port-channel` to observe the basic state of the
aggregation.

```
blackhole.ocf.berkeley.edu(config-if-Po7)#show port-channel
Port Channel Port-Channel5:
  Active Ports: Ethernet10 Ethernet9
Port Channel Port-Channel7:
  No Active Ports
  Configured, but inactive ports:
       Port          Reason unconfigured
    ---------------- -------------------------
       Ethernet13    Waiting for LACP response
       Ethernet14    Waiting for LACP response

```

More details can be found on the EOS guide online, in the [Port Channel section][lacp-guide].

LACP also needs to be configured on the [[host side | doc staff/howto/infrastructure/setting-up-lacp]].

[primary-switch]: https://www.arista.com/assets/data/pdf/Datasheets/7050SX-128_64_Datasheet.pdf
[secondary-switch]: https://www.arista.com/assets/data/pdf/Datasheets/7048T-A_DataSheet.pdf
[stp]: https://en.wikipedia.org/wiki/Bridge_Protocol_Data_Unit
[ipv6-ra]: https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol
[bsecure]: https://bsecure.berkeley.edu
[lacp-guide]: https://www.arista.com/en/um-eos/eos-port-channels-and-lacp
