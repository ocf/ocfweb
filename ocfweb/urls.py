from django.conf.urls import url

from ocfweb.main.home import home
from ocfweb.main.staff_hours import staff_hours


urlpatterns = [
    url('^$', home, name='home'),
    url('^staff-hours$', staff_hours, name='staff-hours'),
]
