import ocflib.account.manage as manage
import ocflib.account.search as search
import ocflib.ucb.directory as directory
from django.forms.forms import NON_FIELD_ERRORS
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from .forms import ApproveForm
from ..calnet.decorators import login_required as calnet_required


@calnet_required
def request_account(request):
    calnet_uid = request.session["calnet_uid"]

    existing_accounts = search.users_by_calnet_uid(calnet_uid)
    real_name = directory.name_by_calnet_uid(calnet_uid)

    if calnet_uid not in settings.TESTER_CALNET_UIDS and existing_accounts:
        return render_to_response("already_requested_account.html", {
            "calnet_uid": calnet_uid,
            "calnet_url": settings.LOGOUT_URL
        })

    if request.method == "POST":
        form = ApproveForm(request.POST)
        if form.is_valid():
            account_name = form.cleaned_data["ocf_login_name"]
            email_address = form.cleaned_data["contact_email"]
            password = form.cleaned_data["password"]

            try:
                manage.queue_creation(real_name, calnet_uid, None,
                                      account_name, email_address,
                                      password)
                manage.trigger_create(settings.ADMIN_SSH_KEY,
                                      settings.CMDS_HOST_KEYS_FILENAME)
            except Exception as e:
                form._errors[NON_FIELD_ERRORS] = form.error_class([str(e)])
            else:
                return render_to_response(
                    "successfully_requested_account.html", {})
    else:
        form = ApproveForm()

    return render_to_response("request_account.html",
                              {
                                  "form": form,
                                  "real_name": real_name
                              }, context_instance=RequestContext(request))
