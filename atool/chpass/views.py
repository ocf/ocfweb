import re
import socket
import syslog

import ocflib.account.manage as manage
import ocflib.account.search as search
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from chpass.forms import ChpassForm
from calnet.decorators import login_required as calnet_required


@calnet_required
def change_password(request):
    calnet_uid = request.session["calnet_uid"]

    accounts = search.users_by_calnet_uid(calnet_uid)

    backend_failures = {}

    if calnet_uid in settings.TESTER_CALNET_UIDS:
        # these test accounts don't have to exist in in LDAP
        accounts.extend(settings.TEST_OCF_ACCOUNTS)

    if request.method == "POST":
        form = ChpassForm(accounts, calnet_uid, request.POST)
        if form.is_valid():
            account = form.cleaned_data["ocf_account"]
            password = form.cleaned_data["new_password"]

            syslog.openlog(str("webchpwd as %s (from %s) for %s" % \
                (calnet_uid, request.META["REMOTE_ADDR"], account)))

            try:
                manage.change_password(account, password, settings.KRB_KEYTAB,
                    "chpass/{}".format(socket.getfqdn()))
                krb_change_success = True
                syslog.syslog("Kerberos password change successful")
            except Exception as e:
                print(e)
                krb_change_success = False
                backend_failures["KRB"] = str(e)
                syslog.syslog("Kerberos password change failed: %s" % e)

            if krb_change_success:
                # deleting this session variable will force
                # the next change_password request to
                # reauthenticate with CalNet
                del request.session["calnet_uid"]

                return render_to_response("successfully_changed_password.html", {
                    "user_account": account
                })
    else:
        form = ChpassForm(accounts, calnet_uid)

    return render_to_response("change_password.html", {
        "form": form,
        "calnet_uid": calnet_uid,
        "backend_failures": backend_failures
    }, context_instance=RequestContext(request))
