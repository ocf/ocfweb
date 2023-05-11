import os
from collections import namedtuple
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import dns.resolver
import requests
from cached_property import cached_property
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from ocflib.infra.hosts import hosts_by_filter

from ocfweb.caching import cache
from ocfweb.docs.doc import Document

PUPPETDB_URL = 'https://puppetdb:8081/pdb/query/v4'
PUPPET_CERT_DIR = os.getenv('PUPPET_CERT_DIR', '/etc/ocfweb/puppet-certs')


class Host(namedtuple('Host', ['hostname', 'type', 'description', 'children'])):
    @classmethod
    def from_ldap(cls: Any, hostname: str, type: str = 'vm', children: Any = ()) -> Any:
        host = hosts_by_filter(f'(cn={hostname})')
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
    def ipv4(self) -> str:
        try:
            # for this and ipv6 below: dns.resolver.query is not typed but is within a package.
            return str(dns.resolver.query(self.hostname, 'A')[0])  # type: ignore
        except dns.resolver.NXDOMAIN:
            return 'No IPv4 Address'

    @cached_property
    def ipv6(self) -> str:
        try:
            return str(dns.resolver.query(self.hostname, 'AAAA')[0])  # type: ignore
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return 'No IPv6 address'

    @cached_property
    def english_type(self) -> str:
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
    def has_munin(self) -> bool:
        return self.type in ('hypervisor', 'vm', 'server', 'desktop')

    def __key(self) -> Tuple[Any, str, str]:
        """Key function used for comparison."""
        ranking = {
            'hypervisor': 1,
            'server': 2,
            'desktop': float('inf'),
        }
        default = 3
        return (ranking.get(self.type, default), self.type, self.hostname)

    def __lt__(self: Any, other_host: Any) -> bool:
        return self.__key() < other_host.__key()


def is_hidden(host: Dict[Any, Any]) -> bool:
    return host['cn'][0].startswith('hozer-') or host['cn'][0].startswith('dev-')


PQL_GET_VMS = "facts { name = 'vms' }"
PQL_IS_HYPERVISOR = 'resources[certname] { type = "Class" and title = "Ocf_kvm" }'


def query_puppet(query: str) -> Dict[Any, Any]:
    """Accepts a PQL query, returns a parsed json result."""
    r = requests.get(
        PUPPETDB_URL,
        cert=(
            os.path.join(PUPPET_CERT_DIR, 'puppet-cert.pem'),
            os.path.join(PUPPET_CERT_DIR, 'puppet-private.pem'),
        ),
        verify=os.path.join(PUPPET_CERT_DIR, 'puppet-ca.pem'),
        params={'query': query},
    )
    return r.json() if r.status_code == 200 else None


def format_query_output(item: Dict[Any, Any]) -> Tuple[Any, Any]:
    """Converts an item of a puppet query to tuple(hostname, query_value)."""
    return item['certname'].split('.')[0], item.get('value')


def ldap_to_host(item: Any) -> Tuple[Any, Any]:
    """Accepts an ldap output item, returns tuple(hostname, host_object)."""
    description = item.get('description', [''])[0]
    hostname = item['cn'][0]
    return hostname, Host(hostname, item['type'], description, ())


@cache()
def get_hosts() -> List[Any]:
    ldap_output = hosts_by_filter('(|(type=server)(type=desktop)(type=printer))')
    servers: Dict[Any, Any] = dict(ldap_to_host(item) for item in ldap_output if not is_hidden(item))

    hypervisors_hostnames: Dict[Any, Any] = dict(format_query_output(item) for item in query_puppet(PQL_IS_HYPERVISOR))
    all_children: Dict[Any, Any] = dict(format_query_output(item) for item in query_puppet(PQL_GET_VMS))

    hostnames_seen = {
        # These are manually added later, with the correct type
        'overheat',
        'tornado',
    }
    servers_to_display = []
    # Add children to hypervisors
    for hypervisor_hostname in hypervisors_hostnames:
        children = []
        for child_hostname in all_children.get(hypervisor_hostname, []):
            child = servers.get(child_hostname)
            if child:
                children.append(child._replace(type='vm'))
                hostnames_seen.add(child.hostname)
        description = servers[hypervisor_hostname].description if hypervisor_hostname in servers else None
        servers_to_display.append(
            Host(
                hostname=hypervisor_hostname,
                type='hypervisor',
                description=description,
                children=children,
            ),
        )
        hostnames_seen.add(hypervisor_hostname)

    # Handle special cases
    for host in servers.values():
        if host.hostname not in hostnames_seen:
            servers_to_display.append(host)

    servers_to_display.extend([
        Host(
            hostname='blackhole',
            type='network',
            description='Arista 7050SX Switch.',
            children=[],
        ),
        servers['overheat']._replace(type='raspi'),
        servers['tornado']._replace(type='nuc'),
    ])

    return sorted(servers_to_display)


def servers(doc: Document, request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'docs/servers.html',
        {
            'title': doc.title,
            'hosts': get_hosts(),
        },
    )
