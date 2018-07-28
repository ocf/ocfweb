[[!meta title="External firewall"]]

We use a Palo Alto Networks (PAN) firewall provided by IST. We have one network
port in the server room which is activated and behind the firewall; we have
another network port activated in the lab behind the television which is also
behind the firewall. All the ports the desktops use are also behind the
firewall since they are routed through the switch in the server room.

## Administering the firewall

### Accessing the interface

Administration of the firewall is done through the [web interface][panorama],
and must be done from an on-campus IP address (for instance through the
[library VPN][library-vpn] or SOCKS proxying through an OCF host). **Remember
to specify https when loading the firewall admin page**, as it does not have a
redirect from http to https. If you are having connection issues with the
firewall admin page loading indefinitely, it is likely because you are trying
to use http or trying to access it from an off-campus IP. To quickly set up a
SOCKS proxy, run `ssh -D 8000 -N supernova` from any off-campus host and then
set up the SOCKS proxy (through your OS or through your browser's settings) to
use the proxy on `localhost` and port `8000`.

[panorama]: https://panorama.net.berkeley.edu
[library-vpn]: http://www.lib.berkeley.edu/using-the-libraries/vpn

To sign in to administer the firewall, make sure to use the single sign-on
(SSO) option, and it will ask for CalNet authentication.

### Policies

All our current policies are located in the "Pre Rules" section under
"Security" in the policies tab. This option should be right at the top in the
box on the left side of the page. It contains all our rules since we are only
blocking traffic (either outgoing or incoming) before it goes through the
firewall, so all we need are pre rules.

In general the interface is pretty self-explanatory. Each rule has a custom
name and a description that describes what kind of traffic it should be
blocking or letting through, as well as the source and destination addresses
(or groups of addresses), application (identified by the firewall), service
(port), and whether it is allowed or blocked. Each rule has a dropdown next to
the rule name if you hover over it that leads to the log viewer, where you can
see what kind of traffic matched each rule and when the traffic was
allowed/blocked.

Any changes made to the firewall policies need to be committed and pushed to
the firewall using the commit button and then the push button (or the commit
and push button to do it in one step) located in the top right.

### Syslog

When we switched over to the new PAN firewall, syslog was set up to send
messages to `syslog.ocf.berkeley.edu`, however it is only configured to send
logs there over TLS, so currently it is failing.
