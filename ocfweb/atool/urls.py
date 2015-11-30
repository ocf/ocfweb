from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


urlpatterns = [
    url(r'^$', lambda _: redirect(reverse('change_password'))),
    url(r'^internal-error/$', lambda _: 1 / 0),

    url(r'^change-password/$', 'ocfweb.atool.chpass.views.change_password',
        name='change_password'),
    url(r'^commands/$', 'ocfweb.atool.cmds.views.commands', name='commands'),

    # account creation
    url(r'^request-account/$', 'ocfweb.atool.approve.views.request_account',
        name='request_account'),
    url(r'^request-account/wait/$', 'ocfweb.atool.approve.views.wait_for_account',
        name='wait_for_account'),
    url(r'^request-account/created/$', 'ocfweb.atool.approve.views.account_created',
        name='account_created'),
    url(r'^request-account/pending/$', 'ocfweb.atool.approve.views.account_pending',
        name='account_pending'),

    # request vhost
    url(r'^request-vhost/$', 'ocfweb.atool.vhost.views.request_vhost',
        name='request_vhost'),
    url(r'^request-vhost/success/$', 'ocfweb.atool.vhost.views.request_vhost_success',
        name='request_vhost_success'),

    # calnet login
    url(r'^calnet/login/$', 'ocfweb.atool.calnet.views.login', name='calnet_login'),
    url(r'^calnet/logout/$', 'ocfweb.atool.calnet.views.logout', name='calnet_logout'),

    # ocf login
    url(r'^login/$', 'ocfweb.atool.ocf.views.login', name='login'),
    url(r'^logout/$', 'ocfweb.atool.ocf.views.logout', name='logout')
]
