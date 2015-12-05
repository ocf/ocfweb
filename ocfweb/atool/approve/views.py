import ocflib.account.search as search
import ocflib.ucb.directory as directory
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from ocflib.account.creation import encrypt_password
from ocflib.account.creation import NewAccountRequest
from ocflib.account.submission import NewAccountResponse

from ocfweb.atool.approve.forms import ApproveForm
from ocfweb.atool.calnet.decorators import login_required as calnet_required
from ocfweb.atool.constants import PASSWORD_ENCRYPTION_PUBKEY
from ocfweb.atool.constants import TESTER_CALNET_UIDS
from ocfweb.atool.ocf.tasks import celery_app
from ocfweb.atool.ocf.tasks import validate_then_create_account


@calnet_required
def request_account(request):
    calnet_uid = request.session['calnet_uid']
    status = 'new_request'

    existing_accounts = search.users_by_calnet_uid(calnet_uid)
    real_name = directory.name_by_calnet_uid(calnet_uid)

    if calnet_uid not in TESTER_CALNET_UIDS and existing_accounts:
        return render_to_response(
            'request-account/already-has-account.html',
            {
                'calnet_uid': calnet_uid,
                'calnet_url': settings.LOGOUT_URL
            },
            context_instance=RequestContext(request)
        )

    if request.method == 'POST':
        form = ApproveForm(request.POST)
        if form.is_valid():
            req = NewAccountRequest(
                user_name=form.cleaned_data['ocf_login_name'],
                real_name=real_name,
                is_group=False,
                calnet_uid=calnet_uid,
                callink_oid=None,
                email=form.cleaned_data['contact_email'],
                encrypted_password=encrypt_password(
                    form.cleaned_data['password'],
                    PASSWORD_ENCRYPTION_PUBKEY,
                ),
                handle_warnings=NewAccountRequest.WARNINGS_WARN,
            )
            if 'warnings-submit' in request.POST:
                req = req._replace(
                    handle_warnings=NewAccountRequest.WARNINGS_SUBMIT,
                )

            task = validate_then_create_account.delay(req)
            task.wait(timeout=5)

            if isinstance(task.result, NewAccountResponse):
                if task.result.status == NewAccountResponse.REJECTED:
                    status = 'has_errors'
                    form._errors[NON_FIELD_ERRORS] = form.error_class(task.result.errors)
                elif task.result.status == NewAccountResponse.FLAGGED:
                    status = 'has_warnings'
                    form._errors[NON_FIELD_ERRORS] = form.error_class(task.result.errors)
                elif task.result.status == NewAccountResponse.PENDING:
                    return HttpResponseRedirect(reverse('account_pending'))
                else:
                    raise AssertionError('Unexpected state reached')
            else:
                # validation was successful, the account is being created now
                request.session['approve_task_id'] = task.result
                return HttpResponseRedirect(reverse('wait_for_account'))
    else:
        form = ApproveForm()

    return render_to_response(
        'request-account/form.html',
        {
            'form': form,
            'real_name': real_name,
            'status': status,
        },
        context_instance=RequestContext(request)
    )


def wait_for_account(request):
    if 'approve_task_id' not in request.session:
        return render_to_response(
            'request-account/wait/error-no-task-id.html', {},
            context_instance=RequestContext(request)
        )

    task = celery_app.AsyncResult(request.session['approve_task_id'])
    if not task.ready():
        meta = task.info
        status = ['Starting creation']
        if isinstance(meta, dict) and 'status' in meta:
            status.extend(meta['status'])
        return render_to_response(
            'request-account/wait/wait.html',
            {
                'status': status,
            },
            context_instance=RequestContext(request)
        )
    elif isinstance(task.result, NewAccountResponse):
        if task.result.status == NewAccountResponse.CREATED:
            return HttpResponseRedirect(reverse('account_created'))
    elif isinstance(task.result, Exception):
        raise task.result

    return render_to_response(
        'request-account/wait/error-probably-not-created.html', {},
        context_instance=RequestContext(request)
    )


def account_pending(request):
    return render_to_response(
        'request-account/pending.html', {},
        context_instance=RequestContext(request)
    )


def account_created(request):
    return render_to_response(
        'request-account/success.html', {},
        context_instance=RequestContext(request)
    )
