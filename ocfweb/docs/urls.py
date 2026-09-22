import re
from typing import Union

from django.conf import settings
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import re_path
from django.views.generic import RedirectView

from ocfweb.docs.doc import Document
from ocfweb.docs.views.servers import servers
from ocfweb.docs.views.shorturl import shorturl

DOCS = {
    doc.name: doc
    for doc in [
        Document(name='/staff/backend/servers', title='Servers', render=servers),
        Document(name='/staff/tips/shorturl-tbl', title='ShortURL table', render=shorturl),
    ]
}

REDIRECTS = {
    '/docs/constitution': '/user-docs/docs/constitution/',
    '/docs/bylaws': '/user-docs/docs/bylaws/',
    '/about': '/user-docs/',
    '/about/formerstaff': '/user-docs/archive/formerstaff/',
    '/communications': '/user-docs/archive/communications/',
    '/communications/blm': '/user-docs/archive/communications/blm/',
    '/communications/stf-renewal': '/user-docs/archive/communications/stf-renewal/',
    '/contact': '/user-docs/contact/',
    '/contact/irc': '/user-docs/contact/chat/',
    '/docs': '/user-docs/docs/',
    '/docs/archive': '/user-docs/archive/',
    '/docs/archive/constitution': '/user-docs/archive/constitution/',
    '/docs/charter': '/user-docs/docs/charter/',
    '/docs/operatingrules': '/user-docs/docs/',
    '/docs/operatingrules/bylaws': '/user-docs/docs/bylaws/',
    '/docs/operatingrules/constitution': '/user-docs/docs/constitution/',
    '/docs/policies': '/user-docs/docs/policies/',
    '/faq': '/user-docs/faq/',
    '/membership': '/user-docs/membership/',
    '/membership/banning': '/user-docs/membership/banning/',
    '/membership/eligibility': '/user-docs/membership/eligibility/',
    '/privacy': '/user-docs/privacy/',
    '/services': '/user-docs/services/',
    '/services/account': '/user-docs/services/account/',
    '/services/account/account-policies': '/user-docs/services/account/account-policy/',
    '/services/account/content-removal': '/user-docs/services/account/content-removal/',
    '/services/hpc': '/user-docs/services/hpc/',
    '/services/hpc/slurm': '/user-docs/services/hpc/slurm/',
    '/services/lab/lab-reservation-policy': '/user-docs/services/lab/lab-reservation-policy/',
    '/services/lab/printing': '/user-docs/services/lab/printing/',
    '/services/mail': '/user-docs/services/mail/',
    '/services/mastodon': '/user-docs/archive/mastodon/',
    '/services/mirrors': '/user-docs/services/mirrors/',
    '/services/mysql': '/user-docs/services/mysql/',
    '/services/shell': '/user-docs/services/shell/',
    '/services/shell/commands': '/user-docs/services/shell/commands/',
    '/services/vhost': '/user-docs/services/vhost/',
    '/services/vhost/badges': '/user-docs/services/vhost/hosting-badges/',
    '/services/vhost/mail': '/user-docs/services/vhost/mail/',
    '/services/vhost/mail/gmail': '/user-docs/services/vhost/mail/gmail/',
    '/services/vhost/subdomain-migration': '/user-docs/services/vhost/subdomain-migration/',
    '/services/web': '/user-docs/services/web/',
    '/services/web/backups': '/user-docs/services/web/backups/',
    '/services/web/django': '/user-docs/services/web/django/',
    '/services/web/flask': '/user-docs/services/web/flask/',
    '/services/web/jekyll': '/user-docs/services/web/jekyll/',
    '/services/web/php': '/user-docs/services/web/php/',
    '/services/web/rails': '/user-docs/services/web/rails/',
    '/services/web/wordpress': '/user-docs/services/web/wordpress/',
    '/services/webapps': '/user-docs/services/webapps/',
    '/services/webapps/nodejs': '/user-docs/services/webapps/nodejs/',
    '/services/webapps/python': '/user-docs/services/webapps/python/',
    '/services/webapps/rails': '/user-docs/services/webapps/rails/',
    '/services/xmpp': '/user-docs/archive/xmpp/',
    '/staff/tips': '/staff-docs/',
    '/staff/tips/desktoprc': '/user-docs/services/lab/desktop-customization/desktoprc/',
    # staff docs, now on the mkdocs site
    '/staff/backend': '/staff-docs/infrastructure/',
    '/staff/backend/backups': '/staff-docs/infrastructure/backups/',
    '/staff/backend/firewall': '/staff-docs/infrastructure/external-firewall/',
    '/staff/backend/git': '/staff-docs/infrastructure/git/',
    '/staff/backend/internal-firewalls': '/staff-docs/infrastructure/debian-hosts/internal-firewalls/',
    '/staff/backend/jenkins': '/staff-docs/infrastructure/debian-hosts/jenkins/',
    '/staff/backend/kerberos': '/staff-docs/infrastructure/kerberos/',
    '/staff/backend/kubernetes': '/staff-docs/infrastructure/kubernetes/',
    '/staff/backend/ldap': '/staff-docs/infrastructure/ldap/',
    '/staff/backend/libvirt': '/staff-docs/infrastructure/debian-hosts/libvirt/',
    '/staff/backend/mail': '/staff-docs/infrastructure/mail/',
    '/staff/backend/mail/vhost': '/staff-docs/infrastructure/mail/vhost/',
    '/staff/backend/munin': '/staff-docs/archive/munin/',
    '/staff/backend/printhost': '/staff-docs/infrastructure/printing/printhost/',
    '/staff/backend/prometheus': '/staff-docs/infrastructure/prometheus/',
    '/staff/backend/puppet': '/staff-docs/infrastructure/debian-hosts/puppet/',
    '/staff/backend/rt': '/staff-docs/rt/',
    '/staff/backend/switch': '/staff-docs/infrastructure/switch/',
    '/staff/getinvolved': '/staff-docs/get-involved/',
    '/staff/i3wm': '/staff-docs/archive/i3wm/',
    '/staff/mailing-lists': '/staff-docs/get-involved/mailing-lists/',
    '/staff/policies': '/staff-docs/policies/',
    '/staff/policies/keycard': '/staff-docs/policies/keycard/',
    '/staff/policies/lab-reservation-policy': '/staff-docs/policies/lab-reservation-policy/',
    '/staff/policies/staff-policy': '/staff-docs/policies/staff-policy/',
    '/staff/powers': '/staff-docs/get-involved/staff-privileges/',
    '/staff/private': '/staff-docs/private/',
    '/staff/procedures': '/staff-docs/',
    '/staff/procedures/accounts': '/staff-docs/accounts/',
    '/staff/procedures/accounts/alumni-reset': '/staff-docs/accounts/alumni-reset/',
    '/staff/procedures/accounts/association': '/staff-docs/accounts/association/',
    '/staff/procedures/accounts/renaming': '/staff-docs/accounts/renaming/',
    '/staff/procedures/backporting-packages': '/staff-docs/infrastructure/debian-hosts/backporting-packages/',
    '/staff/procedures/dmca': '/staff-docs/dmca/',
    '/staff/procedures/editing-docs': '/staff-docs/editing-docs/',
    '/staff/procedures/gapps': '/staff-docs/gapps/',
    '/staff/procedures/granting-privileges': '/staff-docs/get-involved/staff-privileges/granting-privileges/',
    '/staff/procedures/hpc': '/staff-docs/infrastructure/hpc/add-hpc-users/',
    '/staff/procedures/installing-updates': '/staff-docs/infrastructure/debian-hosts/installing-updates/',
    '/staff/procedures/live-resize': '/staff-docs/infrastructure/debian-hosts/live-resize/',
    '/staff/procedures/new-host': '/staff-docs/infrastructure/debian-hosts/new-host/',
    '/staff/procedures/printing': '/staff-docs/infrastructure/printing/maintenance/',
    '/staff/procedures/process-accounting': '/staff-docs/infrastructure/process-accounting/',
    '/staff/procedures/restarting-services': '/staff-docs/infrastructure/debian-hosts/restarting-services/',
    '/staff/procedures/setting-up-lacp': '/staff-docs/infrastructure/debian-hosts/setting-up-lacp/',
    '/staff/procedures/setting-up-mdraid': '/staff-docs/infrastructure/debian-hosts/setting-up-mdraid/',
    '/staff/procedures/ssh-supernova': '/staff-docs/infrastructure/nix-hosts/login-servers/',
    '/staff/procedures/ssl': '/staff-docs/infrastructure/dns/ssl/',
    '/staff/procedures/user-quotas': '/staff-docs/infrastructure/nfs/user-quotas/',
    '/staff/procedures/vhost': '/staff-docs/infrastructure/mail/config-vhost/',
    '/staff/procedures/xmpp': '/staff-docs/archive/xmpp/',
    '/staff/rebuild': '/staff-docs/',
    '/staff/rebuild/rt': '/staff-docs/archive/rt/',
    '/staff/scripts': '/staff-docs/scripts/',
    '/staff/scripts/approve': '/staff-docs/scripts/approve/',
    '/staff/scripts/check': '/staff-docs/scripts/check/',
    '/staff/scripts/checkacct': '/staff-docs/scripts/checkacct/',
    '/staff/scripts/chpass': '/staff-docs/scripts/chpass/',
    '/staff/scripts/economode': '/staff-docs/scripts/economode/',
    '/staff/scripts/how': '/staff-docs/scripts/how/',
    '/staff/scripts/lab-wakeup': '/staff-docs/scripts/lab-wakeup/',
    '/staff/scripts/migrate-vm': '/staff-docs/scripts/migrate-vm/',
    '/staff/scripts/note': '/staff-docs/scripts/note/',
    '/staff/scripts/ocf-tv': '/staff-docs/scripts/ocf-tv/',
    '/staff/scripts/paper': '/staff-docs/scripts/paper/',
    '/staff/scripts/signat': '/staff-docs/scripts/signat/',
    '/staff/scripts/sorry': '/staff-docs/scripts/sorry/',
    '/staff/scripts/ssh-list': '/staff-docs/scripts/ssh-list/',
    '/staff/scripts/unsorry': '/staff-docs/scripts/unsorry/',
    '/staff/startertasks': '/staff-docs/get-involved/starter-tasks/',
    '/staff/startertasks/completed': '/staff-docs/get-involved/starter-tasks/completed/',
    '/staff/techtalks': '/staff-docs/get-involved/techtalks/',
    '/staff/tips/shorturls': '/staff-docs/shorturls/',
    '/staff/tips/staffvm': '/staff-docs/archive/staffvm/',
    '/staff/tips/staffvm/ocfweb': '/staff-docs/archive/staffvm/ocfweb/',
    '/staff/tips/staffvm/znc': '/staff-docs/archive/znc/',
    '/staff/tips/templates': '/staff-docs/rt/templates/',
    '/staff/tips/testaccts': '/staff-docs/testaccts/',
    '/staff/tips/twitch': '/staff-docs/archive/twitch/',
}


def render_doc(request: HttpRequest, doc_name: str) -> HttpResponse:
    """Render a document given a request."""
    doc = DOCS['/' + doc_name]
    if not doc:
        raise Http404()
    return doc.render(doc, request)


def send_redirect(request: HttpRequest, redir_src: str) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
    """Send a redirect to the actual document given the redirecting page."""
    redir_dest = REDIRECTS['/' + redir_src]
    return redirect(settings.DOCS_URL + redir_dest, permanent=True)


def doc_name(doc_name: str) -> str:
    # we can't actually deal with escaping into a regex, so we just use a whitelist
    assert re.match(r'^/[a-zA-Z0-9\-/]+$', doc_name), 'Bad document name: ' + doc_name
    return doc_name[1:].replace('-', '\\-')


doc_names = '|'.join(map(doc_name, DOCS.keys()))
redir_names = '|'.join(map(doc_name, REDIRECTS.keys()))


urlpatterns = [
    re_path(r'^$', RedirectView.as_view(url=settings.DOCS_URL + '/user-docs/', permanent=True)),

    re_path(r'^about/officers/$', RedirectView.as_view(pattern_name='about-officers', permanent=True)),
    re_path(r'^services/lab/$', RedirectView.as_view(pattern_name='lab', permanent=True)),

    # we use a complicated generated regex here so that we have actual
    # validation of URLs (in other words, if you try to make a link to a
    # missing document, it will fail)
    re_path(fr'^({redir_names})/$', send_redirect),
    re_path(fr'^({doc_names})/$', render_doc, name='doc'),
]
