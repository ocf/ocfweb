from django.conf.urls import url

from ocfweb.api import hours
<<<<<<< HEAD
from ocfweb.api import lab
=======
from ocfweb.api import labstats
>>>>>>> labstats -> ocfweb draft wip

urlpatterns = [
    url(r'^hours$', hours.get_hours_all, name='hours_all'),
    url(r'^hours/today$', hours.get_hours_today, name='hours_today'),
    url(r'^lab/desktops$', lab.desktop_usage, name='desktop_usage'),
    url(r'^session/checkin$', labstats.desktop_checkin, name='desktop_checkin'),
]
