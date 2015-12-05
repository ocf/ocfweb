import socket
import syslog

import ocflib.account.manage as manage
from django.shortcuts import render_to_response
from django.template import RequestContext

from ocfweb.atool.calnet.decorators import login_required as calnet_required
from ocfweb.atool.chpass.forms import ChpassForm
from ocfweb.atool.chpass.forms import get_authorized_accounts_for
from ocfweb.atool.constants import KRB_KEYTAB


@calnet_required
def change_password(request):
    calnet_uid = request.session['calnet_uid']
    accounts = get_authorized_accounts_for(calnet_uid)

    backend_failures = {}

    if request.method == 'POST':
        form = ChpassForm(accounts, calnet_uid, request.POST)
        if form.is_valid():
            account = form.cleaned_data['ocf_account']
            password = form.cleaned_data['new_password']

            syslog.openlog(
                str('webchpwd as %s (from %s) for %s' %
                    (calnet_uid, request.META['REMOTE_ADDR'], account)))

            try:
                manage.change_password_with_keytab(
                    account,
                    password,
                    KRB_KEYTAB,
                    'chpass/{}'.format(socket.getfqdn()))
                krb_change_success = True
                syslog.syslog('Kerberos password change successful')
            except Exception as e:
                print(e)
                krb_change_success = False
                backend_failures['KRB'] = str(e)
                syslog.syslog('Kerberos password change failed: %s' % e)

            if krb_change_success:
                # deleting this session variable will force
                # the next change_password request to
                # reauthenticate with CalNet
                del request.session['calnet_uid']

                return render_to_response(
                    'successfully_changed_password.html',
                    {
                        'user_account': account
                    },
                    context_instance=RequestContext(request)
                )
    else:
        form = ChpassForm(accounts, calnet_uid)

    return render_to_response(
        'change_password.html',
        {
            'form': form,
            'calnet_uid': calnet_uid,
            'backend_failures': backend_failures
        },
        context_instance=RequestContext(request)
    )
