from django.urls import re_path

from ocfweb.tv import main

urlpatterns = [
    re_path(r'^$', main.tv_main, name='tv_main'),
    re_path(r'^labmap$', main.tv_labmap, name='tv_labmap'),
]
