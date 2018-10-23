from collections import namedtuple

import dns.resolver
from cached_property import cached_property
from django.shortcuts import render
from ocflib.infra.hosts import hosts_by_filter

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
    # XXX: FOR TESTING PURPOSES ONLY, REMOVE THIS BEFORE MERGING
    puppet_query_output = eval('[ { "name": "vms", "environment": "abizer_aux", "value": [], "certname": "jaws.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [ "fallingrocks", "cataclysm", "dev-flood", "dev-maelstrom", "dev-pestilence", "dev-tsunami", "dev-werewolves", "dev-whiteout", "doom", "fraud", "hozer-62", "limniceruption", "lowgpa", "miasma" ], "certname": "hal.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [], "certname": "mudslide.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [ "pox", "alamo", "apocalypse", "blackrain", "fallout", "falsevacuum", "fireball", "fukushima", "gnats", "leprosy", "malaria", "nuke", "oilspill", "panic", "pileup", "riot", "sarin", "shipwreck", "virus", "vortex", "war", "zerg", "walpurgisnacht", "mudslide", "pompeii", "locusts", "fire", "rapture", "smallpox", "aliens", "cloudburst", "coldwave", "coma", "dev-firestorm", "emp", "meltdown", "meteorite", "old-vampires", "quasar", "ragnarok", "revolution", "sauron", "skynet", "tempest" ], "certname": "pandemic.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [ "nyx", "dementors", "democracy", "whiteout", "reaper", "segfault", "monsoon", "fraud", "gridlock", "lethe", "anthrax", "supernova", "firestorm", "pestilence", "flood", "maelstrom", "thunder", "death", "tsunami", "lightning", "vampires", "werewolves", "biohazard", "cataclysm", "dev-dementors", "dev-flood", "dev-whiteout", "doom", "hozer-69", "hozer-70", "hozer-71", "hozer-73", "hozer-74", "limniceruption", "matrix", "miasma", "zombies" ], "certname": "riptide.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [], "certname": "gnats.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [], "certname": "smallpox.ocf.berkeley.edu" } ]')  # noqa: E501
    for entry in puppet_query_output:
        if entry['certname'].split('.')[0] == host_name:
            return entry['value']
    return []


def is_hidden(host):
    return host['cn'][0].startswith('hozer-') or host['cn'][0].startswith('dev-')


TEMP_GET_CHILDREN = "facts { name = 'vms' }"
TEMP_IS_VIRT_FALSE = "facts { name = 'is_virtual' and value = false }"


def query_puppet(query):
    """Placeholder function for puppet queries
    Accepts a PQL query, returns a dictionary with hostname as keys and
    'value' in the query output as values
    """
    if query == TEMP_IS_VIRT_FALSE:
        output = '[ { "name": "is_virtual", "environment": "production", "certname": "firewhirl.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "outbreak.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "avalanche.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "abizer_aux", "certname": "dataloss.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "bigbang.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "blackout.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "wildfire.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "famine.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "meteorstorm.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "sinkhole.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "abizer", "certname": "hal.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "invasion.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "abizer_aux", "certname": "jaws.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "destruction.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "bzh", "certname": "corruption.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "tornado.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "cyanide.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "plague.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "gleeb", "certname": "drought.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "blizzard.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "acid.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "venom.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "hurricane.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "heatwave.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "chaos.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "volcano.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "blight.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "riptide.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "hailstorm.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "pandemic.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "asteroid.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "headcrash.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "arsenic.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "eruption.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "cooperc", "certname": "madcow.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "cyclone.ocf.berkeley.edu", "value": false }, { "name": "is_virtual", "environment": "production", "certname": "surge.ocf.berkeley.edu", "value": false } ]'  # noqa: E501
        output = eval(output.replace('false', 'False'))
    if query == TEMP_GET_CHILDREN:
        output = eval('[ { "name": "vms", "environment": "abizer_aux", "value": [], "certname": "jaws.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [ "fallingrocks", "cataclysm", "dev-flood", "dev-maelstrom", "dev-pestilence", "dev-tsunami", "dev-werewolves", "dev-whiteout", "doom", "fraud", "hozer-62", "limniceruption", "lowgpa", "miasma" ], "certname": "hal.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [], "certname": "mudslide.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [ "pox", "alamo", "apocalypse", "blackrain", "fallout", "falsevacuum", "fireball", "fukushima", "gnats", "leprosy", "malaria", "nuke", "oilspill", "panic", "pileup", "riot", "sarin", "shipwreck", "virus", "vortex", "war", "zerg", "walpurgisnacht", "mudslide", "pompeii", "locusts", "fire", "rapture", "smallpox", "aliens", "cloudburst", "coldwave", "coma", "dev-firestorm", "emp", "meltdown", "meteorite", "old-vampires", "quasar", "ragnarok", "revolution", "sauron", "skynet", "tempest" ], "certname": "pandemic.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [ "nyx", "dementors", "democracy", "whiteout", "reaper", "segfault", "monsoon", "fraud", "gridlock", "lethe", "anthrax", "supernova", "firestorm", "pestilence", "flood", "maelstrom", "thunder", "death", "tsunami", "lightning", "vampires", "werewolves", "biohazard", "cataclysm", "dev-dementors", "dev-flood", "dev-whiteout", "doom", "hozer-69", "hozer-70", "hozer-71", "hozer-73", "hozer-74", "limniceruption", "matrix", "miasma", "zombies" ], "certname": "riptide.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [], "certname": "gnats.ocf.berkeley.edu" }, { "name": "vms", "environment": "production", "value": [], "certname": "smallpox.ocf.berkeley.edu" } ]')  # noqa: E501
    result = {}
    for d in output:
        hostname = d['certname'].split('.')[0]
        result[hostname] = d['value']
    return result


@periodic(120)
def get_hosts():
    def create_hosts(lst):
        """Accepts a list of raw ldap output, returns a dictionary of host
        objects indexed by hostname
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

    # Add children to hypervisors
    for h in list(servers.values()):
        children = []
        for child_hostname in get_children(h.hostname):
            child = servers.get(child_hostname, False)
            if child:
                del servers[child.hostname]
                children.append(Host(child.hostname, 'vm', child.description, ()))
        if children:
            del servers[h.hostname]
            hypervisors[h.hostname] = Host(
                h.hostname,
                'hypervisor',
                h.description,
                children,
            )

    # Handle special cases
    def change_host_type(hostname, host_type, type_dict):
        """Pop Host with hostname from servers, change its type, and add to misc
        """
        del servers[hostname]
        type_dict[hostname] = Host.from_ldap(hostname, type=host_type)

    change_host_type('overheat', 'raspi', misc)
    change_host_type('tornado', 'nuc', misc)
    change_host_type('jaws', 'hypervisor', hypervisors)
    misc['blackhole'] = Host(
        'blackhole', 'network',
        'Arista 7050SX Switch.', [],
    )

    return [*hypervisors.values(), *servers.values(), *desktops.values(), *misc.values()]


def servers(doc, request):
    return render(
        request,
        'docs/servers.html',
        {
            'title': doc.title,
            'hosts': get_hosts(),
        },
    )
