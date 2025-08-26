from django.conf.urls import include
from django.conf.urls import re_path
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from ocfweb.about.lab import lab_open_source
from ocfweb.about.lab import lab_survey
from ocfweb.about.lab import lab_vote
from ocfweb.about.staff import about_staff
from ocfweb.account.urls import urlpatterns as account
from ocfweb.announcements.urls import urlpatterns as announcements
from ocfweb.api.urls import urlpatterns as api
from ocfweb.docs.urls import urlpatterns as docs
from ocfweb.lab_reservations.urls import urlpatterns as lab_reservations
from ocfweb.login.urls import urlpatterns as login
from ocfweb.main.favicon import favicon
from ocfweb.main.home import home
from ocfweb.main.hosting_logos import hosting_logo
from ocfweb.main.robots import robots_dot_txt
from ocfweb.main.security import security_dot_txt
from ocfweb.main.staff_hours import staff_hours
from ocfweb.stats.urls import urlpatterns as stats
from ocfweb.test.periodic import test_list_periodic_functions
from ocfweb.test.session import test_session
from ocfweb.tv.urls import urlpatterns as tv

urlpatterns = [
    # test pages
    re_path(r'^test/status$', lambda _: HttpResponse('ok'), name='status'),
    re_path(r'^test/session$', test_session, name='test_session'),
    re_path(r'^test/periodic$', test_list_periodic_functions, name='test_list_periodic_functions'),

    # prometheus metrics
    re_path('', include('django_prometheus.urls')),

    re_path(r'^$', home, name='home'),
    re_path(r'^robots\.txt$', robots_dot_txt, name='robots.txt'),
    re_path(r'^favicon.ico$', favicon, name='favicon'),
    re_path(r'^.well-known/security\.txt$', security_dot_txt, name='security.txt'),

    re_path(r'^staff-hours$', staff_hours, name='staff-hours'),

    re_path(r'^account/', include(account)),
    re_path(r'^announcements/', include(announcements)),
    re_path(r'^docs/', include(docs)),
    re_path(r'^login/', include(login)),
    re_path(r'^stats/', include(stats)),
    re_path(r'^lab_reservations/', include(lab_reservations)),

    # about pages
    re_path(r'^about/staff$', about_staff, name='about-staff'),
    re_path(r'^about/lab/open-source$', lab_open_source, name='lab-open-source'),
    re_path(r'^about/lab/vote$', lab_vote, name='lab-vote'),
    re_path(r'^about/lab/survey$', lab_survey, name='lab-survey'),

    # tv endpoints
    re_path(r'^tv/', include(tv)),

    # API endpoints
    re_path(r'^api/', include(api)),

    # hosting logos
    re_path(
        r'^images/hosted-logos/(?:index\.shtml)?$',
        lambda _: redirect(reverse('doc', args=('services/vhost/badges',)), permanent=True),
    ),
    re_path(r'^images/hosted-logos/(.*)$', lambda _, image: redirect('hosting-logo', image, permanent=True)),
    re_path(r'^hosting-logos/(.*)$', hosting_logo, name='hosting-logo'),

    # legacy redirects
    re_path(r'^index\.s?html$', lambda _: redirect(reverse('home'), permanent=True)),
    re_path(r'^staff_hours(?:\.cgi)?$', lambda _: redirect(reverse('staff-hours'), permanent=True)),
    re_path(r'^staff-hours\.cgi$', lambda _: redirect(reverse('staff-hours'), permanent=True)),
    re_path(r'^OCF/(?:index\.shtml)?$', lambda _: redirect(reverse('doc', args=('about',)), permanent=True)),
    re_path(
        r'^OCF/(?:past_)?officers.shtml$',
        lambda _: redirect(reverse('doc', args=('about/officers',)), permanent=True),
    ),
    re_path(r'^OCF/staff/(?:index\.shtml)?$', lambda _: redirect(reverse('doc', args=('staff',)), permanent=True)),
    re_path(
        r'^OCF/staff/where-now\.shtml$',
        lambda _: redirect(reverse('doc', args=('about/formerstaff',)), permanent=True),
    ),
    re_path(r'^OCF/policies(?:/|$)', lambda _: redirect(reverse('docs'), permanent=True)),
    re_path(r'^OCF/OCF_FAQ\.shtml$', lambda _: redirect(reverse('doc', args=('faq',)), permanent=True)),
    re_path(r'^OCF/officers_.*\.s?html$', lambda _: redirect(reverse('doc', args=('about/officers',)), permanent=True)),
    re_path(r'^OCF/staff/how-to-join\.shtml$', lambda _: redirect(reverse('about-staff'), permanent=True)),
    re_path(r'^mlk$', lambda _: redirect(reverse('doc', args=('services/lab',)), permanent=True)),
]
