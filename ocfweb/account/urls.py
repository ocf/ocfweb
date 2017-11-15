from django.conf.urls import url

from ocfweb.account.chpass import change_password
from ocfweb.account.commands import commands
from ocfweb.account.register import account_created
from ocfweb.account.register import account_pending
from ocfweb.account.register import request_account
from ocfweb.account.register import recommend
from ocfweb.account.register import wait_for_account
from ocfweb.account.register import validate
from ocfweb.account.vhost import request_vhost
from ocfweb.account.vhost import request_vhost_success
from ocfweb.account.vhost_mail import vhost_mail
from ocfweb.account.vhost_mail import vhost_mail_csv_export
from ocfweb.account.vhost_mail import vhost_mail_csv_import
from ocfweb.account.vhost_mail import vhost_mail_update


urlpatterns = [
    url(r'^password/$', change_password, name='change_password'),
    url(r'^commands/$', commands, name='commands'),

    # account creation
    url(r'^register/$', request_account, name='register'),
    url(r'^register/wait/$', wait_for_account, name='wait_for_account'),
    url(r'^register/created/$', account_created, name='account_created'),
    url(r'^register/pending/$', account_pending, name='account_pending'),
    url(r'^register/recommend/$', recommend, name='recommend'),
    url(r'^register/validate/$', validate, name='validate'),

    # request vhost
    url(r'^vhost/$', request_vhost, name='request_vhost'),
    url(r'^vhost/success/$', request_vhost_success, name='request_vhost_success'),

    # mail vhost management
    url(r'^vhost/mail/$', vhost_mail, name='vhost_mail'),
    url(r'^vhost/mail/update/$', vhost_mail_update, name='vhost_mail_update'),
    url(r'vhost/mail/import/([0-9a-zA-Z-.]+)/$', vhost_mail_csv_import, name='vhost_mail_csv_import'),
    url(r'vhost/mail/export/([0-9a-zA-Z-.]+)/$', vhost_mail_csv_export, name='vhost_mail_csv_export'),
]
