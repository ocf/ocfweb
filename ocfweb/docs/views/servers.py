import os.path
from collections import namedtuple

import dns.resolver
from cached_property import cached_property
from django.shortcuts import render
from ocflib.infra.hosts import hosts_by_filter
from requests import get

from ocfweb.caching import periodic


class Host(namedtuple('Host', ['hostname', 'type', 'description', 'children'])):
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
        try:
            return str(dns.resolver.query(self.hostname, 'A')[0])
        except dns.resolver.NXDOMAIN:
            return 'No IPv4 Address'

    @cached_property
    def ipv6(self):
        try:
            return str(dns.resolver.query(self.hostname, 'AAAA')[0])
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
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

    def __key(self):
        """Key function used for comparison."""
        ORDER = {
            'hypervisor': 1,
            'server': 2,
            'desktop': float('inf'),
        }
        DEFAULT_ORDER = 3
        return (ORDER.get(self.type, DEFAULT_ORDER), self.type, self.hostname)

    def __lt__(self, other_host):
        return self.__key() < other_host.__key()


def is_hidden(host):
    return host['cn'][0].startswith('hozer-') or host['cn'][0].startswith('dev-')


PQL_GET_VMS = "facts { name = 'vms' }"
PQL_IS_HYPERVISOR = 'resources[certname] { type = "Class" and title = "Ocf_kvm" }'


def query_puppet(query):
    """Accepts a PQL query, returns a parsed json result."""
    PUPPETDB_URL = 'https://puppetdb:8081/pdb/query/v4'
    PUPPET_CERT_DIR = '/etc/ocfweb/puppet-certs'
    r = get(
        PUPPETDB_URL,
        cert=(
            os.path.join(PUPPET_CERT_DIR, 'puppet-cert.pem'),
            os.path.join(PUPPET_CERT_DIR, 'puppet-private.pem'),
        ),
        verify=os.path.join(PUPPET_CERT_DIR, 'puppet-ca.pem'),
        params={'query': query},
    )
    return r.json() if r.status_code == 200 else None


def format_query_output(item):
    """Converts an item of a puppet query to tuple(hostname, query_value).
    """
    return item['certname'].split('.')[0], item.get('value')


def ldap_to_host(item):
    """Accepts an ldap output item, returns tuple(hostname, host_object).
    """
    description = item.get('description', [''])[0]
    hostname = item['cn'][0]
    return hostname, Host(hostname, item['type'], description, ())


@periodic(300)
def get_hosts():
    ldap_output = hosts_by_filter('(|(type=server)(type=desktop)(type=printer))')
    servers = dict(ldap_to_host(item) for item in ldap_output if not is_hidden(item))

    # Handle special cases
    servers['blackhole'] = Host(
        'blackhole', 'network',
        'Arista 7050SX Switch.', [],
    )
    servers['overheat'] = servers['overheat']._replace(type='raspi')
    servers['tornado'] = servers['tornado']._replace(type='nuc')

    hypervisor_hostnames = dict(format_query_output(item) for item in query_puppet(PQL_IS_HYPERVISOR))
    all_children = dict(format_query_output(item) for item in query_puppet(PQL_GET_VMS))

    # Add children to hypervisors
    for h in list(servers.values()):
        if h.hostname in hypervisor_hostnames:
            # Populate a list of children
            children = []
            for child_hostname in all_children.get(h.hostname, []):
                child = servers.get(child_hostname)
                if child:
                    del servers[child.hostname]
                    children.append(child._replace(type='vm'))
            # Associate host with its children and specify type
            del servers[h.hostname]
            servers[h.hostname] = Host(
                hostname=h.hostname,
                type='hypervisor',
                description=h.description,
                children=children,
            )
    return sorted(servers.values())


def servers(doc, request):
    return render(
        request,
        'docs/servers.html',
        {
            'title': doc.title,
            'hosts': get_hosts(),
        },
    )
