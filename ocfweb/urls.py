from django.conf.urls import include
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect

from ocfweb.docs.urls import urlpatterns as docs
from ocfweb.main.favicon import favicon
from ocfweb.main.home import home
from ocfweb.main.hosting_logos import hosting_logo
from ocfweb.main.staff_hours import staff_hours


urlpatterns = [
    # status page used by end-to-end tests to determine when app is ready
    url('^_status$', lambda _: HttpResponse('ok'), name='status'),

    url('^$', home, name='home'),
    url('^favicon.ico$', favicon, name='favicon'),
    url('^staff-hours$', staff_hours, name='staff-hours'),

    # hosting logos
    url(r'^images/hosted-logos/(?:index\.shtml)?$', lambda _: redirect(
        reverse('doc', args=('services/vhost/badges',)), permanent=True)),
    url('^images/hosted-logos/(.*)$', lambda _, image: redirect('hosting_logo', image, permanent=True)),
    url('^hosting-logos/(.*)$', hosting_logo, name='hosting_logo'),

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

    url('^docs', include(docs)),
]
