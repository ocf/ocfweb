from django.conf.urls import url

from ocfweb.api import hours
from ocfweb.api import lab

urlpatterns = [
    url(r'^hours$', hours.get_hours_all, name='hours_all'),
    url(r'^hours/today$', hours.get_hours_today, name='hours_today'),
    url(r'^desktop_usage$', lab.desktop_usage, name='desktop_usage'), 
]
