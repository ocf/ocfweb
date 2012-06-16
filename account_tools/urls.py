from django.conf.urls.defaults import patterns, url
from django.shortcuts import redirect

urlpatterns = patterns('',
    url(r'^/?$', lambda x: redirect("/account_tools/change_password")),
    url(r'^change_password/?$', 'account_tools.chpass.views.change_password'),
    url(r'^commands/?$', 'account_tools.cmds.views.commands', name="account_tools_commands"),
    url(r'^request_account/?$', 'account_tools.approve.views.request_account'),
    url(r'^calnet/login/?$', 'account_tools.calnet.views.login'),
    url(r'^calnet/logout/?$', 'account_tools.calnet.views.logout'),
)
