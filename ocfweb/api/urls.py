from django.urls import path

from ocfweb.api import announce
from ocfweb.api import hours
from ocfweb.api import lab
from ocfweb.api import meeting_hours
from ocfweb.api import session_tracking
from ocfweb.api import shorturls
from ocfweb.api import staff_hours
from ocfweb.api import stats


urlpatterns = [
    path('announce/blog', announce.get_blog_posts, name='blog_posts'),
    path('hours/staff', staff_hours.get_staff_hours, name='staff_hours'),
    path('hours/today', hours.get_hours_today, name='hours_today'),
    path('lab/desktops', lab.desktop_usage, name='desktop_usage'),
    path('lab/num_users', stats.get_num_users_in_lab, name='get_num_users_in_lab'),
    path('lab/staff', stats.get_staff_in_lab, name='get_staff_in_lab'),
    path('meetings/current', meeting_hours.get_current_meeting, name='current_meeting'),
    path('meetings/next', meeting_hours.get_next_meeting, name='next_meeting'),
    path('meetings/list', meeting_hours.get_meetings_list, name='meetings_list'),
    path('session/log', session_tracking.log_session, name='log_session'),
    path('shorturl/<path:slug>', shorturls.bounce_shorturl, name='bounce_shorturl'),
]
