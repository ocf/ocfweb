from django.conf.urls import include
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect

from ocfweb.about.lab import lab_open_source
from ocfweb.about.staff import about_staff
from ocfweb.account.urls import urlpatterns as account
from ocfweb.announcements.urls import urlpatterns as announcements
from ocfweb.api.urls import urlpatterns as api
from ocfweb.docs.urls import urlpatterns as docs
from ocfweb.login.urls import urlpatterns as login
from ocfweb.main.favicon import favicon
from ocfweb.main.home import home
from ocfweb.main.hosting_logos import hosting_logo
from ocfweb.main.robots import robots_dot_txt
from ocfweb.main.staff_hours import staff_hours
from ocfweb.stats.urls import urlpatterns as stats
from ocfweb.test.periodic import test_list_periodic_functions
from ocfweb.test.session import test_session
from ocfweb.tv.tv_hours import tv_hours

urlpatterns = [
    # test pages
    url(r'^test/status$', lambda _: HttpResponse('ok'), name='status'),
    url(r'^test/session$', test_session, name='test_session'),
    url(r'^test/periodic$', test_list_periodic_functions, name='test_list_periodic_functions'),

    url(r'^$', home, name='home'),
    url(r'^robots\.txt$', robots_dot_txt, name='robots.txt'),
    url(r'^favicon.ico$', favicon, name='favicon'),

    url(r'^staff-hours$', staff_hours, name='staff-hours'),

    url(r'^account/', include(account)),
    url(r'^announcements/', include(announcements)),
    url(r'^docs/', include(docs)),
    url(r'^login/', include(login)),
    url(r'^stats/', include(stats)),

    # about pages
    url(r'^about/staff$', about_staff, name='about-staff'),
    url(r'^about/lab/open-source$', lab_open_source, name='lab-open-source'),

    # tv urls
    url(r'^tv/hours$', tv_hours, name='tv-hours'),

    # API endpoints
    url(r'^api/', include(api)),

    # hosting logos
    url(r'^images/hosted-logos/(?:index\.shtml)?$',
        lambda _: redirect(reverse('doc', args=('services/vhost/badges',)), permanent=True)),
    url(r'^images/hosted-logos/(.*)$', lambda _, image: redirect('hosting-logo', image, permanent=True)),
    url(r'^hosting-logos/(.*)$', hosting_logo, name='hosting-logo'),

    # legacy redirects
    url(r'^index\.s?html$', lambda _: redirect(reverse('home'), permanent=True)),
    url(r'^staff_hours(?:\.cgi)?$', lambda _: redirect(reverse('staff-hours'), permanent=True)),
    url(r'^staff-hours\.cgi$', lambda _: redirect(reverse('staff-hours'), permanent=True)),
    url(r'^OCF/(?:index\.shtml)?$', lambda _: redirect(reverse('doc', args=('about',)), permanent=True)),
    url(r'^OCF/(?:past_)?officers.shtml$',
        lambda _: redirect(reverse('doc', args=('about/officers',)), permanent=True)),
    url(r'^OCF/staff/(?:index\.shtml)?$', lambda _: redirect(reverse('doc', args=('staff',)), permanent=True)),
    url(r'^OCF/staff/where-now\.shtml$',
        lambda _: redirect(reverse('doc', args=('about/formerstaff',)), permanent=True)),
    url(r'^OCF/policies(?:/|$)', lambda _: redirect(reverse('docs'), permanent=True)),
    url(r'^OCF/OCF_FAQ\.shtml$', lambda _: redirect(reverse('doc', args=('faq',)), permanent=True)),
    url(r'^OCF/officers_.*\.s?html$', lambda _: redirect(reverse('doc', args=('about/officers',)), permanent=True)),
    url(r'^OCF/staff/how-to-join\.shtml$', lambda _: redirect(reverse('about-staff'), permanent=True)),
    url(r'^mlk$', lambda _: redirect(reverse('doc', args=('services/lab',)), permanent=True)),
]
