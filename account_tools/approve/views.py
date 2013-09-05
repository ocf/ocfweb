from django.forms.forms import NON_FIELD_ERRORS
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from approve.forms import ApproveForm, GroupApproveForm
from approve.ocf_approve import approve_user, approve_group, ApprovalError
from ocf.decorators import https_required
from ocf.utils import users_by_calnet_uid, get_student_groups, get_student_group_name
from calnet.decorators import login_required as calnet_required
from calnet.utils import name_by_calnet_uid


@https_required
@calnet_required
def request_account(request):
    calnet_uid = request.session["calnet_uid"]

    existing_accounts = users_by_calnet_uid(calnet_uid)
    real_name = name_by_calnet_uid(calnet_uid)

    if calnet_uid not in settings.TESTER_CALNET_UIDS and len(existing_accounts):
        return render_to_response("already_requested_account.html", {
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
                approve_user(real_name, calnet_uid, account_name,
                             email_address, password, forward = forward_mail)
            except ApprovalError as e:
                form._errors[NON_FIELD_ERRORS] = form.error_class([str(e)])
            else:
                return render_to_response("successfully_requested_account.html",
                                          {})
    else:
        form = ApproveForm()

    return render_to_response("request_account.html",
        {
        "form": form,
        "real_name": real_name
        }, context_instance=RequestContext(request))

@https_required
@calnet_required
def request_group_account(request):
    calnet_uid = request.session["calnet_uid"]

    existing_accounts = users_by_calnet_uid(calnet_uid)
    responsible = name_by_calnet_uid(calnet_uid)

    if calnet_uid not in settings.TESTER_CALNET_UIDS and len(existing_accounts):
        return render_to_response("already_requested_account.html", {
            "calnet_uid": calnet_uid,
            "calnet_url": settings.LOGOUT_URL
        })

    if request.method == "POST":
        form = GroupApproveForm(request.POST, calnet_uid = calnet_uid)
        if form.is_valid():
            account_name = form.cleaned_data["ocf_login_name"]
            email_address = form.cleaned_data["contact_email"]
            forward_mail = form.cleaned_data["forward_email"]
            password = form.cleaned_data["password"]
            callink_oid = form.cleaned_data["student_groups"]
            group_name = get_student_group_name(int(callink_oid))

            try:
                approve_group(group_name, responsible, callink_oid, email_address, account_name,
                    password, forward = False)
            except ApprovalError as e:
                form._errors[NON_FIELD_ERRORS] = form.error_class([str(e)])
            else:
                return render_to_response("successfully_requested_account.html",
                                          {})
    else:
        form = GroupApproveForm(calnet_uid = calnet_uid)

    return render_to_response("request_group_account.html",
        {
        "form": form,
        "real_name": responsible
        }, context_instance=RequestContext(request))
