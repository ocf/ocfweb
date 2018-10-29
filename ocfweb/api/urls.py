from django.urls import path

from ocfweb.api import hours
from ocfweb.api import lab
from ocfweb.api import session_tracking

urlpatterns = [
    path('hours', hours.get_hours_all, name='hours_all'),
    path('hours/today', hours.get_hours_today, name='hours_today'),
    path('lab/desktops', lab.desktop_usage, name='desktop_usage'),
    path('session/log', session_tracking.log_session, name='log_session'),
    path('lab/staff', lab.visible_staff, name='visible_staff'),
]
