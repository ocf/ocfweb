from django.conf.urls import url

from ocfweb.main.favicon import favicon
from ocfweb.main.home import home
from ocfweb.main.lab import lab
from ocfweb.main.staff_hours import staff_hours


urlpatterns = [
    url('^$', home, name='home'),
    url('^favicon.ico$', favicon, name='favicon'),
    url('^staff-hours$', staff_hours, name='staff-hours'),
    url('^lab$', lab, name='lab'),
]
