from collections import namedtuple

import dns.resolver
from cached_property import cached_property
from django.shortcuts import render
from ocflib.infra.hosts import hosts_by_filter
from requests import get

from ocfweb.caching import periodic


class Host(namedtuple('Host', ['hostname', 'type', 'description', 'children'])):

    # TODO: don't hard-code host types or children

    @classmethod
    def from_ldap(cls, hostname, type='vm', children=()):
        host = hosts_by_filter('(cn={})'.format(hostname))
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


def is_hidden(host):
    return host['cn'][0].startswith('hozer-') or host['cn'][0].startswith('dev-')


PQL_GET_CHILDREN = "facts { name = 'vms' }"
PQL_IS_HYPERVISOR = 'resources[certname] { type = "Class" and title = "Ocf_kvm" }'


def query_puppet(query):
    """Accepts a PQL query, returns a dictionary with hostname as keys and
    'value' in the query output as values
    """
    URL = 'https://puppetdb:8081/pdb/query/v4'
    ROOT_DIR = '/etc/ocfweb/'
    r = get(
        URL, cert=(ROOT_DIR + 'puppet-cert.pem', ROOT_DIR + 'puppet-private.pem'),
        verify=ROOT_DIR + 'puppet-ca.pem', params={'query': query},
    )
    output = eval(r.text)
    result = {}
    for d in output:
        hostname = d['certname'].split('.')[0]
        result[hostname] = d.get('value')
    return result


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


@periodic(300)
def get_hosts():
    servers = create_hosts(hosts_by_filter('(type=server)'))
    desktops = create_hosts(hosts_by_filter('(type=desktop)'))
    misc = create_hosts(hosts_by_filter('(type=printer)'))
    hypervisors = {}

    hypervisor_hostnames = query_puppet(PQL_IS_HYPERVISOR)
    all_children = query_puppet(PQL_GET_CHILDREN)

    # Add children to hypervisors
    for h in list(servers.values()):
        if h.hostname in hypervisor_hostnames:
            # Populate a list of children
            children = []
            for child_hostname in all_children.get(h.hostname, []):
                child = servers.get(child_hostname)
                if child:
                    del servers[child.hostname]
                    children.append(Host(child.hostname, 'vm', child.description, ()))
            # Associate host with its children and move it to the hypervisors dictionary
            del servers[h.hostname]
            hypervisors[h.hostname] = Host(
                h.hostname,
                'hypervisor',
                h.description,
                children,
            )

    # Handle special cases
    def change_host_type(hostname, host_type, origin_type_dict, target_type_dict):
        """Pop Host with hostname from servers, change its type, and add to misc
        """
        host = origin_type_dict.pop(hostname)
        target_type_dict[hostname] = host._replace(type=host_type)

    change_host_type('overheat', 'raspi', servers, misc)
    change_host_type('tornado', 'nuc', servers, misc)
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
