from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from approve.forms import ApproveForm
from approve.utils import run_approve
from ocf.decorators import https_required
from ocf.utils import users_by_calnet_uid
from calnet.decorators import login_required as calnet_required
from calnet.utils import name_by_calnet_uid

@https_required
@calnet_required
def request_account(request):
    calnet_uid = request.session["calnet_uid"]

    existing_accounts = users_by_calnet_uid(calnet_uid)
    real_name = name_by_calnet_uid(calnet_uid)

    if calnet_uid not in settings.TESTER_CALNET_UIDS and len(existing_accounts):
        return render_to_response("already_requested_account", {
            "calnet_uid": calnet_uid,
            "calnet_url": settings.LOGOUT_URL
        })

    if request.method == "POST":
        form = ApproveForm(request.POST)
        if form.is_valid():
            account_name = form.cleaned_data["ocf_login_name"]
            email_address = form.cleaned_data["contact_email"]
            forward_mail = form.cleaned_data["forward_email"]
            password = form.cleaned_data["password"]
            try:
                run_approve(real_name, calnet_uid, account_name,\
                    email_address, forward_mail, password)
            except Exception as e:
                if not "__all__" in form.errors:
                    form.errors["__all__"] = []

                form.errors["__all__"].append(str(e))
    else:
        form = ApproveForm()

    return render_to_response("request_account.html",{
        "form": form,
        "form_action": request.get_full_path(),
        "real_name": real_name
    }, context_instance=RequestContext(request))
