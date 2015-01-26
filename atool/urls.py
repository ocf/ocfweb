from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

urlpatterns = [
    url(r'^/?$', lambda _: redirect(reverse("change_password"))),
    url(r'^change-password$', 'atool.chpass.views.change_password',
        name="change_password"),
    url(r'^commands$', 'atool.cmds.views.commands', name="commands"),
    url(r'^request-account$', 'atool.approve.views.request_account',
        name="request_account"),
    url(r'^request-vhost$', 'atool.vhost.views.request_vhost',
        name="request_vhost"),
    url(r'^request-vhost/success$', 'atool.vhost.views.request_vhost_success',
        name="request_vhost_success"),
    url(r'^calnet/login$', 'atool.calnet.views.login', name="calnet_login"),
    url(r'^calnet/logout$', 'atool.calnet.views.logout', name="calnet_logout"),
    url(r'^login$', 'atool.ocf.views.login', name="login"),
    url(r'^logout$', 'atool.ocf.views.logout', name="logout")
]
