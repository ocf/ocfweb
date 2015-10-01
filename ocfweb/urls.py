import re

from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect

from ocfweb.docs.docs import doc
from ocfweb.docs.docs import docs_index
from ocfweb.docs.docs import list_doc_names
from ocfweb.main.favicon import favicon
from ocfweb.main.home import home
from ocfweb.main.hosting_logos import hosting_logo
from ocfweb.main.servers import servers
from ocfweb.main.staff_hours import staff_hours


def doc_name(doc_name):
    # we can't actually deal with escaping into a regex, so we just use a whitelist
    assert re.match('^/[a-zA-Z\-/]+$', doc_name)
    return doc_name[1:].replace('-', '\-')

doc_names = '|'.join(map(doc_name, list_doc_names()))

urlpatterns = [
    url('^_status$', lambda _: HttpResponse('ok'), name='status'),

    url('^$', home, name='home'),
    url('^favicon.ico$', favicon, name='favicon'),
    url('^staff-hours$', staff_hours, name='staff-hours'),
    url('^servers$', servers, name='servers'),

    # hosting logos
    url('^images/hosted-logos/(.*)$', lambda _, image: redirect('hosting_logo', image, permanent=True)),
    url('^hosting-logos/(.*)$', hosting_logo, name='hosting_logo'),

    url('^docs/$', docs_index, name='docs'),
    # we use a complicated generated regex here so that we have actual
    # validation of URLs (in other words, if you try to make a link to a
    # missing document, it will fail)
    url('^docs/({doc_names})/$'.format(doc_names=doc_names), doc, name='doc'),

    # legacy redirects
    url(r'^index\.s?html$', lambda _: redirect(reverse('home'), permanent=True)),
    url(r'^staff_hours(?:\.cgi)?$', lambda _: redirect(reverse('staff-hours'), permanent=True)),
    url(r'^staff-hours\.cgi$', lambda _: redirect(reverse('staff-hours'), permanent=True)),
    url(r'^OCF/(?:index\.shtml)?$', lambda _: redirect(reverse('doc', args=('about',)), permanent=True)),
    url(r'^OCF/(?:past_)?officers.shtml$', lambda _:
        redirect(reverse('doc', args=('about/officers',)),
                 permanent=True
                 )),
    url(r'^OCF/staff/(?:index\.shtml)?$', lambda _: redirect(reverse('doc', args=('staff',)), permanent=True)),
    url(r'^OCF/staff/where-now\.shtml$', lambda _:
        redirect(reverse('doc', args=('about/formerstaff',)),
                 permanent=True
                 )),
    url(r'^OCF/policies(?:/|$)', lambda _: redirect(reverse('docs'), permanent=True)),
    url(r'^OCF/OCF_FAQ\.shtml$', lambda _: redirect(reverse('doc', args=('faq',)), permanent=True)),
    url(r'^OCF/officers_.*\.s?html$', lambda _: redirect(reverse('doc', args=('about/officers',)), permanent=True)),
    url(r'^OCF/staff/how-to-join\.shtml$', lambda _: redirect(
        'https://hello.ocf.berkeley.edu/',
        permanent=True
    )),
]
