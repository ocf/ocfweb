from django.urls import re_path

from ocfweb.login.calnet import login as calnet_login
from ocfweb.login.calnet import logout as calnet_logout
from ocfweb.login.ocf import login
from ocfweb.login.ocf import logout


urlpatterns = [
    re_path(r'^login/$', login, name='login'),
    re_path(r'^logout/$', logout, name='logout'),

    re_path(r'^calnet/login/$', calnet_login, name='calnet_login'),
    re_path(r'^calnet/logout/$', calnet_logout, name='calnet_logout'),
]
