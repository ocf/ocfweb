from django.conf.urls import url

from ocfweb.stats.accounts import cumulative_accounts_graph
from ocfweb.stats.accounts import cumulative_group_accounts_graph
from ocfweb.stats.accounts import stats_accounts
from ocfweb.stats.daily_graph import daily_graph_image
from ocfweb.stats.printing import pages_printed
from ocfweb.stats.printing import semester_histogram
from ocfweb.stats.printing import stats_printing
from ocfweb.stats.session_count import session_count_image
from ocfweb.stats.session_length import session_length_image
from ocfweb.stats.summary import summary


urlpatterns = [
    url(r'^$', summary, name='stats'),
    url(r'^daily-graph/graph$', daily_graph_image, name='daily_graph_image'),
    url(r'^session-count/graph$', session_count_image, name='session_count_image'),
    url(r'^session-length/graph$', session_length_image, name='session_length_image'),
    url(r'^printing/$', stats_printing, name='stats_printing'),
    url(r'^accounts/$', stats_accounts, name='stats_accounts'),
    url(r'^accounts/cumulative/graph$', cumulative_accounts_graph, name='cumulative_accounts_graph'),
    url(
        r'^accounts/cumulative-groups/graph$',
        cumulative_group_accounts_graph,
        name='cumulative_group_accounts_graph',
    ),
    url(r'^printing/semester-histogram/graph$', semester_histogram, name='semester_histogram'),
    url(r'^printing/pages-printed$', pages_printed, name='pages_printed'),
]
