from django.conf.urls import url

from ocfweb.main.home import home


urlpatterns = [
    url('^$', home, name='home'),
    url('^staff-hours$', home, name='staff-hours'),
]
