from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

urlpatterns = [
    url(r'^/?$', lambda _: redirect(reverse('change_password'))),
    url(r'^internal-error$', lambda _: 1 / 0),

    url(r'^change-password$', 'atool.chpass.views.change_password',
        name='change_password'),
    url(r'^commands$', 'atool.cmds.views.commands', name='commands'),

    # account creation
    url(r'^request-account$', 'atool.approve.views.request_account',
        name='request_account'),
    url(r'^request-account/wait$', 'atool.approve.views.wait_for_account',
        name='wait_for_account'),
    url(r'^request-account/created$', 'atool.approve.views.account_created',
        name='account_created'),
    url(r'^request-account/pending$', 'atool.approve.views.account_pending',
        name='account_pending'),

    # request vhost
    url(r'^request-vhost$', 'atool.vhost.views.request_vhost',
        name='request_vhost'),
    url(r'^request-vhost/success$', 'atool.vhost.views.request_vhost_success',
        name='request_vhost_success'),

    # calnet login
    url(r'^calnet/login$', 'atool.calnet.views.login', name='calnet_login'),
    url(r'^calnet/logout$', 'atool.calnet.views.logout', name='calnet_logout'),

    # ocf login
    url(r'^login$', 'atool.ocf.views.login', name='login'),
    url(r'^logout$', 'atool.ocf.views.logout', name='logout')
]
