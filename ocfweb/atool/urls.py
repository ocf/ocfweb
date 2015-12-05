from django.conf.urls import url

from ocfweb.atool.approve.views import account_created
from ocfweb.atool.approve.views import account_pending
from ocfweb.atool.approve.views import request_account
from ocfweb.atool.approve.views import wait_for_account
from ocfweb.atool.calnet.views import calnet_login
from ocfweb.atool.calnet.views import calnet_logout
from ocfweb.atool.chpass.views import change_password
from ocfweb.atool.cmds.views import commands
from ocfweb.atool.ocf.views import login
from ocfweb.atool.ocf.views import logout
from ocfweb.atool.vhost.views import request_vhost
from ocfweb.atool.vhost.views import request_vhost_success


urlpatterns = [
    url(r'^change-password/$', change_password, name='change_password'),
    url(r'^commands/$', commands, name='commands'),

    # account creation
    url(r'^request-account/$', request_account, name='request_account'),
    url(r'^request-account/wait/$', wait_for_account, name='wait_for_account'),
    url(r'^request-account/created/$', account_created, name='account_created'),
    url(r'^request-account/pending/$', account_pending, name='account_pending'),

    # request vhost
    url(r'^request-vhost/$', request_vhost, name='request_vhost'),
    url(r'^request-vhost/success/$', request_vhost_success, name='request_vhost_success'),

    # calnet login
    url(r'^calnet/login/$', calnet_login, name='calnet_login'),
    url(r'^calnet/logout/$', calnet_logout, name='calnet_logout'),

    # ocf login
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout')
]
