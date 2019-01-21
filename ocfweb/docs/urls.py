import re
from itertools import chain

from django.conf.urls import url
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from ocfweb.docs.doc import Document
from ocfweb.docs.markdown_based import get_markdown_docs
from ocfweb.docs.views.account_policies import account_policies
from ocfweb.docs.views.buster_upgrade import buster_upgrade
from ocfweb.docs.views.commands import commands
from ocfweb.docs.views.hosting_badges import hosting_badges
from ocfweb.docs.views.index import docs_index
from ocfweb.docs.views.index import staffdocs_index
from ocfweb.docs.views.lab import lab
from ocfweb.docs.views.officers import officers
from ocfweb.docs.views.servers import servers


DOCS = {
    doc.name: doc
    for doc in chain(
        [
            Document(name='/about/officers', title='Officers', render=officers),
            Document(name='/staff/backend/servers', title='Servers', render=servers),
            Document(name='/staff/backend/buster', title='Debian Buster upgrade', render=buster_upgrade),
            Document(name='/services/account/account-policies', title='Account policies', render=account_policies),
            Document(name='/services/vhost/badges', title='Hosting badges', render=hosting_badges),
            Document(name='/services/lab', title='Computer lab', render=lab),
            Document(name='/services/shell/commands', title='Command reference', render=commands),
        ],
        get_markdown_docs(),
    )
}

REDIRECTS = {
    '/docs/constitution': 'docs/operatingrules/constitution',
    '/docs/bylaws': 'docs/operatingrules/bylaws',

    '/staff/backend/git': 'staff/howto/development/git',
    '/staff/rebuild/rt': 'staff/rt',
    '/staff/backend/libvirt': 'staff/howto/infrastructure/libvirt',
    '/staff/i3wm': 'staff/howto/other/i3wm',
    '/staff/procedures': 'staff/howto',
    '/staff/scripts': 'staff/howto',
    '/staff/procedures/accounts/association': 'staff/howto/account-management/association',
    '/staff/scripts/check': 'staff/howto/account-management/check',
    '/staff/scripts/checkacct': 'staff/howto/account-management/checkacct',
    '/staff/scripts/chpass': 'staff/howto/account-management/chpass',
    '/staff/scripts/note': 'staff/howto/account-management/note',
    '/staff/procedures/process-accounting': 'staff/howto/account-management/process-accounting',
    '/staff/scripts/signat': 'staff/howto/account-management/signat',
    '/staff/scripts/sorry': 'staff/howto/account-management/sorry',
    '/staff/scripts/unsorry': 'staff/howto/account-management/unsorry',
    '/staff/procedures/user-quotas': 'staff/howto/account-management/user-quotas',
    '/staff/procedures/backporting-packages': 'staff/howto/development/backporting-packages',
    '/staff/procedures/editing-docs': 'staff/howto/development/editing-docs',
    '/staff/procedures/installing-updates': 'staff/howto/infrastructure/installing-updates',
    '/staff/scripts/migrate-vm': 'staff/howto/infrastructure/migrate-vm',
    '/staff/procedures/new-host': 'staff/howto/infrastructure/new-host',
    '/staff/procedures/restarting-services': 'staff/howto/infrastructure/restarting-services',
    '/staff/procedures/setting-up-lacp': 'staff/howto/infrastructure/setting-up-lacp',
    '/staff/procedures/setting-up-mdraid': 'staff/howto/infrastructure/setting-up-mdraid',
    '/staff/scripts/ssh-list': 'staff/howto/infrastructure/ssh-list',
    '/staff/procedures/ssl': 'staff/howto/infrastructure/ssl',
    '/staff/scripts/economode': 'staff/howto/maintenance/economode',
    '/staff/scripts/lab-wakeup': 'staff/howto/maintenance/lab-wakeup',
    '/staff/procedures/printing': 'staff/howto/maintenance/printing',
    '/staff/procedures/dmca': 'staff/howto/other/dmca',
    '/staff/scripts/how': 'staff/howto/other/how',
    '/staff/scripts/ocf-tv': 'staff/howto/other/ocf-tv',
    '/staff/scripts/pdf-open': 'staff/howto/other/pdf-open',
    '/staff/procedures/gapps': 'staff/howto/staff-admin/gapps',
    '/staff/procedures/granting-privileges': 'staff/howto/staff-admin/granting-privileges',
    '/staff/procedures/accounts/alumni-reset': 'staff/howto/user-services/alumni-reset',
    '/staff/scripts/approve': 'staff/howto/user-services/approve',
    '/staff/scripts/paper': 'staff/howto/user-services/paper',
    '/staff/procedures/vhost': 'staff/howto/user-services/vhost',

}


def render_doc(request, doc_name):
    """Render a document given a request."""
    doc = DOCS['/' + doc_name]
    if not doc:
        raise Http404()
    return doc.render(doc, request)


def send_redirect(request, redir_src):
    """Send a redirect to the actual document given the redirecting page."""
    redir_dest = REDIRECTS['/' + redir_src]
    return redirect(reverse('doc', args=(redir_dest,)), permanent=True)


def doc_name(doc_name):
    # we can't actually deal with escaping into a regex, so we just use a whitelist
    assert re.match(r'^/[a-zA-Z0-9\-/]+$', doc_name), 'Bad document name: ' + doc_name
    return doc_name[1:].replace('-', r'\-')


doc_names = '|'.join(map(doc_name, DOCS.keys()))
redir_names = '|'.join(map(doc_name, REDIRECTS.keys()))


urlpatterns = [
    url(r'^$', docs_index, name='docs'),
    url(r'staff/$', staffdocs_index, name='staffdocs'),

    # we use a complicated generated regex here so that we have actual
    # validation of URLs (in other words, if you try to make a link to a
    # missing document, it will fail)
    url(r'^({redir_names})/$'.format(redir_names=redir_names), send_redirect),
    url(r'^({doc_names})/$'.format(doc_names=doc_names), render_doc, name='doc'),
]
