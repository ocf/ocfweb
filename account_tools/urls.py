from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

urlpatterns = [
    url(r'^/?$', lambda _: redirect(reverse("change_password"))),
    url(r'^change-password$', 'account_tools.chpass.views.change_password', name="change_password"),
    url(r'^commands$', 'account_tools.cmds.views.commands', name="commands"),
    url(r'^request-account$', 'account_tools.approve.views.request_account', name="request_account"),
    url(r'^request-vhost$', 'account_tools.vhost.views.request_vhost', name="request_vhost"),
    url(r'^request-vhost/success$', 'account_tools.vhost.views.request_vhost_success', name="request_vhost_success"),
    url(r'^calnet/login$', 'account_tools.calnet.views.login', name="calnet_login"),
    url(r'^calnet/logout$', 'account_tools.calnet.views.logout', name="calnet_logout"),
    url(r'^login$', 'account_tools.ocf.views.login', name="login"),
    url(r'^logout$', 'account_tools.ocf.views.logout', name="logout")
]
