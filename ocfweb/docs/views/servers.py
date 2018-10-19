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
            'raspi': 'Raspberry Pi',
            'server': 'Physical Server',
            'vip': 'Virtual IP',
            'vm': 'Virtual Machine',
        }[self.type]

    @cached_property
    def has_munin(self):
        return self.type in ('hypervisor', 'vm', 'server', 'desktop')

def get_children(host_name):
    """Get the children of a host in a list
    Right now this returns a hard-coded entry from puppet query. Would be changed
    once I figure out how to query puppet from python.
    """
    puppet_query_output = eval('[ { "name": "vms", "environment": "abizer_aux", "value": [], "certname": "jaws.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [ "fallingrocks", "cataclysm", "dev-flood", "dev-maelstrom", "dev-pestilence", "dev-tsunami", "dev-werewolves", "dev-whiteout", "doom", "fraud", "hozer-62", "limniceruption", "lowgpa", "miasma" ], "certname": "hal.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [], "certname": "mudslide.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [ "pox", "alamo", "apocalypse", "blackrain", "fallout", "falsevacuum", "fireball", "fukushima", "gnats", "leprosy", "malaria", "nuke", "oilspill", "panic", "pileup", "riot", "sarin", "shipwreck", "virus", "vortex", "war", "zerg", "walpurgisnacht", "mudslide", "pompeii", "locusts", "fire", "rapture", "smallpox", "aliens", "cloudburst", "coldwave", "coma", "dev-firestorm", "emp", "meltdown", "meteorite", "old-vampires", "quasar", "ragnarok", "revolution", "sauron", "skynet", "tempest" ], "certname": "pandemic.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [ "nyx", "dementors", "democracy", "whiteout", "reaper", "segfault", "monsoon", "fraud", "gridlock", "lethe", "anthrax", "supernova", "firestorm", "pestilence", "flood", "maelstrom", "thunder", "death", "tsunami", "lightning", "vampires", "werewolves", "biohazard", "cataclysm", "dev-dementors", "dev-flood", "dev-whiteout", "doom", "hozer-69", "hozer-70", "hozer-71", "hozer-73", "hozer-74", "limniceruption", "matrix", "miasma", "zombies" ], "certname": "riptide.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [], "certname": "gnats.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [], "certname": "smallpox.ocf.berkeley.edu" } ]')
    for entry in puppet_query_output:
        if entry['certname'].split('.')[0] == host_name:
            return entry['value']
    return []

@periodic(120)
def get_hosts():
    return [
        Host.from_ldap(
            hostname='hal',
            type='hypervisor',
            children=[
                Host.from_ldap(hostname)
                for hostname in (
                    'fallingrocks',
                    'monsoon',
                )
            ],
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
                    'democracy',
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
                    'zombies',
                )
            ],
        ),

        Host.from_ldap(
            hostname='pandemic',
            type='hypervisor',
            children=[
                Host.from_ldap(hostname)
                for hostname in (
                    'pileup',
                )
            ],
        ),

        Host.from_ldap(
            hostname='riptide',
            type='hypervisor',
        ),

        Host.from_ldap(
            hostname='corruption',
            type='server',
        ),

        Host('blackhole', 'network', 'Managed Cisco Catalyst 2960S-48TS-L Switch.', []),

        Host('logjam', 'printer', '', []),
        Host('pagefault', 'printer', '', []),
        Host('papercut', 'printer', '', []),
        Host.from_ldap('overheat', type='raspi'),
        Host.from_ldap('tornado', type='nuc'),

        *(Host.from_ldap(desktop, type='desktop')
          for desktop in sorted(list_desktops())),
    ]

    is_hidden = lambda host: host['cn'][0][:6] == 'hozer-' or host['cn'][0][:4] == 'dev-'
    
    def create_hosts(lst):
        """Accepts a list of raw ldap output, returns a dictionary of host objects indexed by hostname
        """
        hosts = {}
        for h in lst:
            if not is_hidden(h):
                description = h.get('description', [''])[0]
                hostname = h['cn'][0]
                hosts[hostname] = (Host(hostname, h['type'], description, ()))
        return hosts

    servers = create_hosts(hosts_by_filter('(type=server)'))
    desktops = create_hosts(hosts_by_filter('(type=desktop)'))
    misc = create_hosts(hosts_by_filter('(type=printer)'))
    hypervisors = {}

def servers(doc, request):
    return render(
        request,
        'docs/servers.html',
        {
            'title': doc.title,
            'hosts': get_hosts(),
        },
    )
