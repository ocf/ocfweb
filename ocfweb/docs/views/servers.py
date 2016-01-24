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
    def from_ldap(cls, hostname, type='vm'):
        host, = hosts_by_filter('(cn={})'.format(hostname))
        if 'description' in host:
            description, = host['description']
        else:
            description = ''
        return Host(
            hostname=hostname,
            type=type,
            description=description,
            children=[],
        )

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


@periodic(120)
def get_hosts():
    return [
        Host(
            hostname='hal',
            type='hypervisor',
            description='KVM hypervisor for staff/testing VMs',
            children=[
                Host.from_ldap(hostname)
                for hostname in ['dev-death', 'supernova']
            ],
        ),

        Host(
            hostname='jaws',
            type='hypervisor',
            description='KVM hypervisor for most production VMs',
            children=[
                Host.from_ldap(hostname)
                for hostname in [
                    'anthrax',
                    'coma',
                    'dementors',
                    'firestorm',
                    'flood',
                    'lightning',
                    'maelstrom',
                    'pestilence',
                    'pollution',
                    'reaper',
                    'sandstorm',
                    'typhoon',
                    'zombies',
                ]
            ],
        ),

        Host(
            hostname='pandemic',
            type='hypervisor',
            description='NFS host, KVM hypervisor for most NFS-using VMs',
            children=[
                Host.from_ldap(hostname)
                for hostname in ['biohazard', 'death', 'tsunami']
            ],
        ),

        Host.from_ldap('fallingrocks'),

        Host('blackhole', 'network', 'Managed Cisco Catalyst 2960S-48TS-L Switch', []),

        Host('deforestation', 'printer', '', []),
        Host('logjam', 'printer', '', []),
    ] + [
        Host.from_ldap(desktop, type='desktop')
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
