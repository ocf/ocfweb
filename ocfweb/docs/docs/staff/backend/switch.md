
[[!meta title="Managed switches"]]

We use an [Arista 7050SX-64][primary-switch] 10GbE switch as a primary switch
for our servers, and two [Arista 7048T-A][secondary-switch] 1GbE switches for
desktops and management respectively. These devices were donated to us by
Arista Networks in Fall 2018. Each device in the lab connects first to the back
of a patch panel, and then from a port on the patch panel to a port on one of
the 7048T-As via Cat6. The servers connect directly to the 7050SX via SFP+ DACs,
as does our uplink to IST, through a Cat6 to 1GbE SFP+ converter. The 7048T's
connect to the 7050SX through their SFP+ uplink ports.

Currently, our switches operate as unmanaged devices, merely providing layer 2
connectivity. Our previous switch, a Cisco Catalyst 2960S, was used for some
time to drop [Spanning-tree protocol BPDUs][stp] and [IPv6 Router Advertisements][ipv6-ra]
on all ports, as they caused network configuration problems on our end (creating loops
with IST, or hosts autoconfiguring themselves via SLAAC), however, we have since moved
that functionality to our upstream firewall.

In the future, we'd like to make use of some of the more advanced features
available on our switches, such as Port Security, to do things like preventing
desktops from spoofing servers, or using layer 3 functionality to support NAT on
the desktops and other devices.

## Administering the switch

For the time being, administering the switches can only be done by connecting
to them directly via a USB serial console cable. The switches run Arista EOS.

TODO: add some more details about configuring the switch

[primary-switch]: https://www.arista.com/assets/data/pdf/Datasheets/7050SX-128_64_Datasheet.pdf
[secondary-switch]: https://www.arista.com/assets/data/pdf/Datasheets/7048T-A_DataSheet.pdf
[stp]: https://en.wikipedia.org/wiki/Bridge_Protocol_Data_Unit
[ipv6-ra]: https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol
