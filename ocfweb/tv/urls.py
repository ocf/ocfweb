from django.conf.urls import url

from ocfweb.tv import tv_hours

urlpatterns = [
    url(r'^hours/$', tv_hours.tv_hours, name='tv-hours'),
]
