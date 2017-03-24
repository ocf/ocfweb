from django.conf.urls import url

from ocfweb.api import api

urlpatterns = [
    url(r'hours', api.hours, name='hours'),
]
