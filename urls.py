from django.conf.urls.defaults import *
from django.shortcuts import redirect

urlpatterns = patterns('',
    (r'^/?$', lambda x: redirect("/account_tools/change_password")),
    (r'^request_account/?$', 'approve.views.request_account'),
    (r'^change_password/?$', 'chpass.views.change_password'),
    (r'^calnet/login/?$', 'calnet.views.login'),
    (r'^calnet/logout/?$', 'calnet.views.logout'),
)
