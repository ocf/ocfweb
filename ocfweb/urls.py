from django.conf.urls import include
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect

from ocfweb.about.lab import lab_open_source
from ocfweb.about.staff import about_staff
from ocfweb.account.urls import urlpatterns as account
from ocfweb.docs.urls import urlpatterns as docs
from ocfweb.login.urls import urlpatterns as login
from ocfweb.main.favicon import favicon
from ocfweb.main.home import home
from ocfweb.main.hosting_logos import hosting_logo
from ocfweb.main.printing_announcement import printing_announcement
from ocfweb.main.renaming_announcement import renaming_announcement
from ocfweb.main.robots import robots_dot_txt
from ocfweb.main.staff_hours import staff_hours
from ocfweb.stats.accounts import accounts_created_each_day_graph
from ocfweb.stats.accounts import cumulative_accounts_graph
from ocfweb.stats.accounts import cumulative_group_accounts_graph
from ocfweb.stats.accounts import stats_accounts
from ocfweb.stats.daily_graph import daily_graph_image
from ocfweb.stats.printing import semester_histogram
from ocfweb.stats.printing import stats_printing
from ocfweb.stats.sessions import sessions_image
from ocfweb.stats.summary import summary
from ocfweb.test.periodic import test_list_periodic_functions
from ocfweb.test.session import test_session


urlpatterns = [
    # test pages
    url(r'^test/status$', lambda _: HttpResponse('ok'), name='status'),
    url(r'^test/session$', test_session, name='test_session'),
    url(r'^test/periodic$', test_list_periodic_functions, name='test_list_periodic_functions'),

    url(r'^$', home, name='home'),
    url(r'^robots\.txt$', robots_dot_txt, name='robots.txt'),
    url(r'^favicon.ico$', favicon, name='favicon'),
    url(r'^staff-hours$', staff_hours, name='staff-hours'),

    # announcements
    url(r'^announcements/2016-02-09/printing$', printing_announcement, name='printing-announcement'),
    url(r'^announcements/2016-04-01/renaming-ocf$', renaming_announcement, name='renaming-announcement'),

    # about pages
    url(r'^about/staff$', about_staff, name='about-staff'),
    url(r'^about/lab/open-source$', lab_open_source, name='lab-open-source'),

    # hosting logos
    url(r'^images/hosted-logos/(?:index\.shtml)?$',
        lambda _: redirect(reverse('doc', args=('services/vhost/badges',)), permanent=True)),
    url(r'^images/hosted-logos/(.*)$', lambda _, image: redirect('hosting-logo', image, permanent=True)),
    url(r'^hosting-logos/(.*)$', hosting_logo, name='hosting-logo'),

    # stats
    url(r'^stats/$', summary, name='stats'),
    url(r'^stats/daily-graph/graph$', daily_graph_image, name='daily_graph_image'),
    url(r'^stats/sessions/graph$', sessions_image, name='sessions_image'),
    url(r'^stats/printing/$', stats_printing, name='stats_printing'),
    url(r'^stats/accounts/$', stats_accounts, name='stats_accounts'),
    url(r'^stats/accounts/cumulative/graph$', cumulative_accounts_graph, name='cumulative_accounts_graph'),
    url(
        r'^stats/accounts/cumulative-groups/graph$',
        cumulative_group_accounts_graph,
        name='cumulative_group_accounts_graph',
    ),
    url(r'^stats/accounts/daily/graph$', accounts_created_each_day_graph, name='accounts_created_each_day_graph'),
    url(r'^stats/printing/semester-histogram/graph$', semester_histogram, name='semester_histogram'),

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

    url(r'^docs/', include(docs)),

    url(r'^account/', include(account)),

    url(r'^login/', include(login)),
]
