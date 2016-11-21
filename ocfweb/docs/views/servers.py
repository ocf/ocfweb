from collections import namedtuple

import dns.resolver
from cached_property import cached_property
from django.shortcuts import render
from ocflib.infra.hosts import hosts_by_filter
from ocflib.lab.stats import list_desktops

from ocfweb.caching import periodic


class Host(namedtuple('Host', ['hostname', 'type', 'description', 'children'])):

    # TODO: don't hard-code host types or children

    @classmethod
    def from_ldap(cls, hostname, type='vm', children=()):
        host, = hosts_by_filter('(cn={})'.format(hostname))
        if 'description' in host:
            description, = host['description']
        else:
            description = ''
        return cls(
            hostname=hostname,
            type=type,
            description=description,
            children=children,
        )

    @cached_property
    def ipv4(self):
        return str(dns.resolver.query(self.hostname, 'A')[0])

    @cached_property
    def ipv6(self):
        try:
            return str(dns.resolver.query(self.hostname, 'AAAA')[0])
        except dns.resolver.NoAnswer:
            return 'No IPv6 address'

    @cached_property
    def english_type(self):
        return {
            'desktop': 'Desktop',
            'hypervisor': 'Hypervisor',
            'network': 'Networking Gear',
            'nuc': 'NUC',
            'printer': 'Printer',
            'server': 'Physical Server',
            'vip': 'Virtual IP',
            'vm': 'Virtual Machine',
        }[self.type]

    @cached_property
    def has_munin(self):
        return self.type in ('hypervisor', 'vm', 'server', 'desktop')


@periodic(120)
def get_hosts():
    return [
        Host.from_ldap(
            hostname='hal',
            type='hypervisor',
            children=[
                Host.from_ldap(hostname)
                for hostname in (
                    'monsoon',
                )
            ]
        ),

        Host.from_ldap(
            hostname='jaws',
            type='hypervisor',
            children=[
                Host.from_ldap(hostname)
                for hostname in (
                    'anthrax',
                    'biohazard',
                    'death',
                    'dementors',
                    'firestorm',
                    'flood',
                    'lightning',
                    'maelstrom',
                    'pestilence',
                    'reaper',
                    'supernova',
                    'thunder',
                    'tsunami',
                    'werewolves',
                    'whirlwind',
                    'whiteout',
                )
            ],
        ),

        Host.from_ldap(
            hostname='pandemic',
            type='hypervisor',
            children=[
                Host.from_ldap(hostname)
                for hostname in (
                    'fallingrocks',
                    'pileup',
                    'zombies',
                )
            ],
        ),

        Host('blackhole', 'network', 'Managed Cisco Catalyst 2960S-48TS-L Switch.', []),

        Host('logjam', 'printer', '', []),
        Host('pagefault', 'printer', '', []),
        Host('papercut', 'printer', '', []),
        Host.from_ldap('tornado', type='nuc'),
    ] + [
        Host.from_ldap(desktop, type='desktop')
        for desktop in list_desktops()
    ]


def servers(doc, request):
    return render(
        request,
        'docs/servers.html',
        {
            'title': doc.title,
            'hosts': get_hosts(),
        },
    )
