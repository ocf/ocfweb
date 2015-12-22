import ocflib.account.search as search
import ocflib.account.validators as validators
import ocflib.misc.validators
import ocflib.ucb.directory as directory
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ocflib.account.creation import encrypt_password
from ocflib.account.creation import NewAccountRequest
from ocflib.account.submission import NewAccountResponse

from ocfweb.account.constants import PASSWORD_ENCRYPTION_PUBKEY
from ocfweb.account.constants import TESTER_CALNET_UIDS
from ocfweb.auth import calnet_required
from ocfweb.component.celery import celery_app
from ocfweb.component.celery import validate_then_create_account
from ocfweb.component.forms import wrap_validator


@calnet_required
def request_account(request):
    calnet_uid = request.session['calnet_uid']
    status = 'new_request'

    existing_accounts = search.users_by_calnet_uid(calnet_uid)
    real_name = directory.name_by_calnet_uid(calnet_uid)

    if calnet_uid not in TESTER_CALNET_UIDS and existing_accounts:
        return render(
            request,
            'register/already-has-account.html',
            {
                'calnet_uid': calnet_uid,
                'calnet_url': settings.LOGOUT_URL
            },
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

    return render(
        request,
        'register/index.html',
        {
            'form': form,
            'real_name': real_name,
            'status': status,
        },
    )


def wait_for_account(request):
    if 'approve_task_id' not in request.session:
        return render(
            request,
            'register/wait/error-no-task-id.html', {},
        )

    task = celery_app.AsyncResult(request.session['approve_task_id'])
    if not task.ready():
        meta = task.info
        status = ['Starting creation']
        if isinstance(meta, dict) and 'status' in meta:
            status.extend(meta['status'])
        return render(
            request,
            'register/wait/wait.html',
            {
                'status': status,
            },
        )
    elif isinstance(task.result, NewAccountResponse):
        if task.result.status == NewAccountResponse.CREATED:
            return HttpResponseRedirect(reverse('account_created'))
    elif isinstance(task.result, Exception):
        raise task.result

    return render(
        request,
        'register/wait/error-probably-not-created.html', {},
    )


def account_pending(request):
    return render(
        request,
        'register/pending.html', {},
    )


def account_created(request):
    return render(
        request,
        'register/success.html', {},
    )


class ApproveForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ApproveForm, self).__init__(*args, **kwargs)

    ocf_login_name = forms.CharField(
        label='OCF login name',
        validators=[wrap_validator(validators.validate_username)],
        min_length=3,
        max_length=8)

    # password is validated in clean since we need the username as part of the
    # password validation (to compare similarity)
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        label='New password',
        min_length=8,
        max_length=64,
    )

    verify_password = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        label='Confirm password',
        min_length=8,
        max_length=64,
    )
    contact_email = forms.EmailField(
        label='Contact e-mail',
        validators=[wrap_validator(ocflib.misc.validators.valid_email)])

    verify_contact_email = forms.EmailField(label='Confirm contact e-mail')

    disclaimer_agreement = forms.BooleanField(
        label='You have read, understood, and agreed to our policies.',
        error_messages={
            'required': 'You did not agree to our policies.'
        })

    def clean_verify_password(self):
        password = self.cleaned_data.get('password')
        verify_password = self.cleaned_data.get('verify_password')

        if password and verify_password:
            if password != verify_password:
                raise forms.ValidationError("Your passwords don't match.")
        return verify_password

    def clean_verify_contact_email(self):
        email = self.cleaned_data.get('contact_email')
        verify_contact_email = self.cleaned_data.get('verify_contact_email')

        if email and verify_contact_email:
            if email != verify_contact_email:
                raise forms.ValidationError("Your emails don't match.")
        return verify_contact_email

    def clean(self):
        cleaned_data = super(ApproveForm, self).clean()

        # validate password (requires username to check similarity)
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            wrap_validator(validators.validate_password)(username, password)
