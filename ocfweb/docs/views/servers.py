from collections import namedtuple

import dns.resolver
from cached_property import cached_property
from django.shortcuts import render
from ocflib.lab.stats import list_desktops

from ocfweb.caching import cache


class Host(namedtuple('Host', ['hostname', 'type', 'description', 'children'])):

    @cached_property
    def ip(self):
        return str(dns.resolver.query(self.hostname, 'A')[0])

    @cached_property
    def english_type(self):
        return {
            'hypervisor': 'Hypervisor',
            'vm': 'Virtual Machine',
            'server': 'Physical Server',
            'printer': 'Printer',
            'network': 'Networking Gear',
            'desktop': 'Desktop',
        }[self.type]

    @cached_property
    def has_munin(self):
        return self.type in {'hypervisor', 'vm', 'server', 'desktop'}


@cache(ttl=300)
def get_hosts():
    return [
        Host(
            hostname='hal',
            type='hypervisor',
            description='KVM hypervisor for staff/testing VMs',
            children=[
                Host('dev-death', 'vm', 'Web server (staging environment)', []),
                Host('dev-earthquake', 'vm', 'atool (accounts.ocf Django app) (staging environment)', []),
                Host('supernova', 'vm', 'Staff login server, create worker host', []),
            ]
        ),

        Host(
            hostname='jaws',
            type='hypervisor',
            description='KVM hypervisor for most production VMs',
            children=[
                Host('anthrax', 'vm', 'postfix (OCF staff/system mail)', []),
                Host('coma', 'vm', 'ocfweb (ocf.berkeley.edu website)', []),
                Host('dementors', 'vm', 'munin, lab stats (stats.ocf)', []),
                Host('earthquake', 'vm', 'atool (accounts.ocf Django app)', []),
                Host('firestorm', 'vm', 'Kerberos and LDAP', []),
                Host('flood', 'vm', 'IRC host', []),
                Host('lightning', 'vm', 'Puppet host', []),
                Host('maelstrom', 'vm', 'MySQL host', []),
                Host('pestilence', 'vm', 'DNS, DHCP, and PXE', []),
                Host('pollution', 'vm', 'Print server (CUPS, PyKota)', []),
                Host('reaper', 'vm', 'Jenkins', []),
                Host('sandstorm', 'vm', 'Legacy mail server (student groups)', []),
                Host('typhoon', 'vm', 'Request Tracker', []),
                Host('zombies', 'vm', 'CS:GO server', []),
            ],
        ),

        Host(
            hostname='pandemic',
            type='hypervisor',
            description='NFS host, KVM hypervisor for most NFS-using VMs',
            children=[
                Host('biohazard', 'vm', 'Application hosting server (public)', []),
                Host('death', 'vm', 'Web server (public)', []),
                Host('tsunami', 'vm', 'Login server (SSH, public)', []),
            ],
        ),

        Host('fallingrocks', 'server', 'Open-source software mirror, apt repo', []),

        Host('blackhole', 'network', 'Managed Cisco Catalyst 2960S-48TS-L Switch', []),

        Host('deforestation', 'printer', '', []),
        Host('logjam', 'printer', '', []),
    ] + [
        Host(desktop, 'desktop', '', [])
        for desktop in list_desktops()
    ]


def servers(doc, request):
    return render(
        request,
        'servers.html',
        {
            'title': doc.title,
            'hosts': get_hosts(),
        },
    )
