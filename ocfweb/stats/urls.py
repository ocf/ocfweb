from django.urls import re_path

from ocfweb.stats.accounts import stats_accounts
from ocfweb.stats.daily_graph import daily_graph_image
from ocfweb.stats.job_frequency import daily_jobs_image
from ocfweb.stats.mirrors import stats_mirrors
from ocfweb.stats.printing import pages_printed
from ocfweb.stats.printing import semester_histogram
from ocfweb.stats.printing import stats_printing
from ocfweb.stats.semester_job import weekday_jobs_image
from ocfweb.stats.semester_job import weekend_jobs_image
from ocfweb.stats.session_count import session_count_image
from ocfweb.stats.session_length import session_length_image
from ocfweb.stats.session_stats import session_stats
from ocfweb.stats.summary import summary

urlpatterns = [
    re_path(r'^$', summary, name='stats'),
    re_path(r'^daily-graph/graph$', daily_graph_image, name='daily_graph_image'),
    re_path(r'^session-count/graph$', session_count_image, name='session_count_image'),
    re_path(r'^session-length/graph$', session_length_image, name='session_length_image'),
    re_path(r'^printing/$', stats_printing, name='stats_printing'),
    re_path(r'^accounts/$', stats_accounts, name='stats_accounts'),
    re_path(r'^printing/semester-histogram/graph$', semester_histogram, name='semester_histogram'),
    re_path(r'^printing/pages-printed$', pages_printed, name='pages_printed'),
    re_path(r'^printing/daily-job/graph$', daily_jobs_image, name='daily_job_image'),
    re_path(r'^printing/weekend-jobs/graph$', weekend_jobs_image, name='weekend_jobs_image'),
    re_path(r'^printing/weekday-jobs/graph$', weekday_jobs_image, name='weekday_jobs_image'),

    re_path(r'^mirrors/$', stats_mirrors, name='stats_mirrors'),
    re_path(r'^session-stats/$', session_stats, name='session-stats'),
]
