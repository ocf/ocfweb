import time

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

from atool.approve.forms import ApproveForm
from atool.calnet.decorators import login_required as calnet_required
from atool.ocf.tasks import celery_app
from atool.ocf.tasks import create_account


# TODO: this timeout won't work with a global lock on account creation
def wait_for_validation(task, timeout=5):
    """Wait for account validation to finish.

    This doesn't mean the account is created, just that it's passed the
    validation stage. The rest of the waiting is done asynchronously once we're
    guaranteed the account can actually be created.
    """
    start = time.time()
    while time.time() < start + timeout:
        if task.state in ('VALIDATED', 'SUCCESS'):
            return
        time.sleep(0.1)
    else:
        raise RuntimeError('Timed out waiting for validation.')


@calnet_required
def request_account(request):
    calnet_uid = request.session['calnet_uid']
    status = 'new_request'

    existing_accounts = search.users_by_calnet_uid(calnet_uid)
    real_name = directory.name_by_calnet_uid(calnet_uid)

    if calnet_uid not in settings.TESTER_CALNET_UIDS and existing_accounts:
        return render_to_response('already_requested_account.html', {
            'calnet_uid': calnet_uid,
            'calnet_url': settings.LOGOUT_URL
        })

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
                    settings.PASSWORD_ENCRYPTION_PUBKEY,
                ),
                handle_warnings=NewAccountRequest.WARNINGS_WARN,
            )
            if 'warnings-submit' in request.POST:
                req = req._replace(
                    handle_warnings=NewAccountRequest.WARNINGS_SUBMIT,
                )

            task = create_account.delay(req)
            wait_for_validation(task)

            if task.ready():
                if task.result.status == NewAccountResponse.REJECTED:
                    status = 'has_errors'
                    form._errors[NON_FIELD_ERRORS] = form.error_class(task.result.errors)
                elif task.result.status == NewAccountResponse.FLAGGED:
                    status = 'has_warnings'
                    form._errors[NON_FIELD_ERRORS] = form.error_class(task.result.errors)
                elif task.result.status == NewAccountResponse.PENDING:
                    # TODO: this should redirect
                    return render_to_response('successfully_requested_account.html', {})
                else:
                    raise AssertionError('Unexpected state reached')
            else:
                # validation was successful, the account is being created now
                request.session['approve_task_id'] = task.id
                return HttpResponseRedirect(reverse('wait_for_account'))

#            return render_to_response(
#                'successfully_requested_account.html', {})
    else:
        form = ApproveForm()

    return render_to_response('request_account.html',
                              {
                                  'form': form,
                                  'real_name': real_name,
                                  'status': status,
                              }, context_instance=RequestContext(request))


def wait_for_account(request):
    from django.http import HttpResponse
    if 'approve_task_id' not in request.session:
        # TODO: this
        return

    task = celery_app.AsyncResult(request.session['approve_task_id'])
    meta = task.info
    if not task.ready():
        if isinstance(meta, dict) and 'status' in meta:
            return HttpResponse(meta['status'])
    else:
        return HttpResponse('done waiting!')
