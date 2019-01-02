import json
from collections import namedtuple
from os.path import join

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


def is_hidden(host):
    return host['cn'][0].startswith('hozer-') or host['cn'][0].startswith('dev-')


PQL_GET_CHILDREN = "facts { name = 'vms' }"
PQL_IS_HYPERVISOR = 'resources[certname] { type = "Class" and title = "Ocf_kvm" }'


def query_puppet(query):
    """Accepts a PQL query, returns a parsed json result"""
    URL = 'https://puppetdb:8081/pdb/query/v4'
    ROOT_DIR = '/etc/ocfweb/puppet-certs'
    r = get(
        URL,
        cert=(join(ROOT_DIR, 'puppet-cert.pem'), join(ROOT_DIR, 'puppet-private.pem')),
        verify=join(ROOT_DIR, 'puppet-ca.pem'),
        params={'query': query},
    )
    return json.loads(r.text)


def format_query_output(output):
    """Converts the output of a puppet query to a dictionary of the form {certname: value}
    """
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


def host_key(h):
    """Key function for sorting Host objects
    """
    if h.type == 'hypervisor':
        return 'a' + h.hostname
    if h.type == 'server':
        return 'b' + h.hostname
    if h.type == 'desktop':
        return 'z' + h.hostname
    return 'c' + h.type + h.hostname


@periodic(300)
def get_hosts():
    servers = create_hosts(hosts_by_filter('(|(type=server)(type=desktop)(type=printer))'))

    # Handle special cases
    servers['blackhole'] = Host(
        'blackhole', 'network',
        'Arista 7050SX Switch.', [],
    )
    servers['overheat'] = servers['overheat']._replace(type='raspi')
    servers['tornado'] = servers['tornado']._replace(type='nuc')

    hypervisor_hostnames = format_query_output(query_puppet(PQL_IS_HYPERVISOR))
    all_children = format_query_output(query_puppet(PQL_GET_CHILDREN))

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
    return sorted(servers.values(), key=host_key)


def servers(doc, request):
    return render(
        request,
        'docs/servers.html',
        {
            'title': doc.title,
            'hosts': get_hosts(),
        },
    )
