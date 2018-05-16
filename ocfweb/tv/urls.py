from django.conf.urls import url

from ocfweb.tv import main

urlpatterns = [
    url(r'^$', main.tv_main, name='tv_main'),
    url(r'^labmap$', main.tv_labmap, name='tv_labmap'),
]
