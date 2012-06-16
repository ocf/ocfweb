from django.conf.urls.defaults import *
from django.shortcuts import redirect

urlpatterns = patterns('',
    (r'^/?$', lambda x: redirect("/account_tools/change_password")),
    (r'^change_password/?$', 'account_tools.chpass.views.change_password'),
    (r'^commands/?$', 'account_tools.cmds.views.commands'),
    (r'^request_account/?$', 'account_tools.approve.views.request_account'),
    (r'^calnet/login/?$', 'account_tools.calnet.views.login'),
    (r'^calnet/logout/?$', 'account_tools.calnet.views.logout'),
)
