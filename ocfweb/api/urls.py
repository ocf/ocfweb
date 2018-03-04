from django.conf.urls import url

from ocfweb.api import hours
from ocfweb.api import lab
from ocfweb.api import session_tracking

urlpatterns = [
    url(r'^hours$', hours.get_hours_all, name='hours_all'),
    url(r'^hours/today$', hours.get_hours_today, name='hours_today'),
    url(r'^lab/desktops$', lab.desktop_usage, name='desktop_usage'),
    url(r'^session/log$', session_tracking.log_session, name='log_session'),
]
