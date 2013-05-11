from django.conf.urls.defaults import patterns, url
from django.shortcuts import redirect

urlpatterns = patterns('',
    url(r'^/?$', lambda x: redirect("/account_tools/change_password")),
    url(r'^change_password/?$', 'account_tools.chpass.views.change_password', name="change_password"),
    url(r'^commands/?$', 'account_tools.cmds.views.commands', name="commands"),
    url(r'^request_account/?$', 'account_tools.approve.views.request_account', name="request_account"),
    url(r'^request_group_account/?$', 'account_tools.approve.views.request_group_account', name="request_group_account"),
    url(r'^calnet/login/?$', 'account_tools.calnet.views.login', name="calnet_login"),
    url(r'^calnet/logout/?$', 'account_tools.calnet.views.logout', name="calnet_logout"),
)
