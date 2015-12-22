from django.conf.urls import url

from ocfweb.account.chpass import change_password
from ocfweb.account.commands import commands
from ocfweb.account.register import account_created
from ocfweb.account.register import account_pending
from ocfweb.account.register import request_account
from ocfweb.account.register import wait_for_account
from ocfweb.account.vhost import request_vhost
from ocfweb.account.vhost import request_vhost_success


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
]
