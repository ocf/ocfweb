from django.conf.urls import patterns, url
from django.shortcuts import redirect

urlpatterns = patterns('',
    url(r'^/?$', lambda x: redirect("/account_tools/change_password")),
    url(r'^change_password/?$', 'account_tools.chpass.views.change_password', name="change_password"),
    url(r'^commands/?$', 'account_tools.cmds.views.commands', name="commands"),
    url(r'^request_account/?$', 'account_tools.approve.views.request_account', name="request_account"),
    url(r'^request_group_account/?$', 'account_tools.approve.views.request_group_account', name="request_group_account"),
    url(r'^request_vhost/?$', 'account_tools.vhost.views.request_vhost', name="request_vhost"),
    url(r'^request_vhost/success$', 'account_tools.vhost.views.request_vhost_success', name="request_vhost_success"),
    url(r'^calnet/login/?$', 'account_tools.calnet.views.login', name="calnet_login"),
    url(r'^calnet/logout/?$', 'account_tools.calnet.views.logout', name="calnet_logout"),
    url(r'^login$', 'account_tools.ocf.views.login', name="login"),
    url(r'^logout$', 'account_tools.ocf.views.logout', name="logout"),
    url(r'^group_accounts_only$', 'account_tools.ocf.views.group_accounts_only', name='group_accounts_only')
)
