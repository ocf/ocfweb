from typing import Any
from typing import Iterator
from typing import List

from django import forms
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from ocflib.account.search import user_exists
from ocflib.account.search import users_by_calnet_uid
from ocflib.ucb.directory import name_by_calnet_uid
from ocflib.ucb.groups import groups_by_student_signat
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout

from ocfweb.account.constants import TEST_OCF_ACCOUNTS
from ocfweb.account.constants import TESTER_CALNET_UIDS
from ocfweb.auth import calnet_required
from ocfweb.component.celery import change_password as change_password_task
from ocfweb.component.forms import Form

CALLINK_ERROR_MSG = (
    "Couldn't connect to CalLink API. Resetting group "
    'account passwords online is unavailable.'
)


def get_accounts_signatory_for(calnet_uid: str) -> List[Any]:
    def flatten(lst: Iterator[Any]) -> List[Any]:
        return [item for sublist in lst for item in sublist]

    group_accounts = flatten(
        map(
            lambda group: group['accounts'],
            groups_by_student_signat(calnet_uid).values(),
        ),
    )

    # sanity check since we don't trust CalLink API that much:
    # if >= 10 groups, can't change online, sorry
    assert len(group_accounts) < 10, 'should be less than 10 group accounts'

    return group_accounts


def get_accounts_for(calnet_uid: str) -> List[Any]:
    accounts = users_by_calnet_uid(calnet_uid)

    if calnet_uid in TESTER_CALNET_UIDS:
        # these test accounts don't have to exist in in LDAP
        accounts.extend(TEST_OCF_ACCOUNTS)

    return accounts


@calnet_required
def change_password(request: HttpRequest) -> HttpResponse:
    calnet_uid = request.session['calnet_uid']
    error = None
    accounts = get_accounts_for(calnet_uid)
    try:
        accounts += get_accounts_signatory_for(calnet_uid)
    except (ConnectionError, ReadTimeout):
        error = CALLINK_ERROR_MSG

    if not accounts and error is None:
        error = mark_safe(
            render_to_string(
                'account/partials/chpass-no-accounts.html',
                {
                    'calnet_uid': calnet_uid,
                },
            ),
        )

    if request.method == 'POST':
        form = ChpassForm(accounts, calnet_uid, request.POST)
        if form.is_valid():
            account = form.cleaned_data['ocf_account']
            password = form.cleaned_data['new_password']

            try:
                calnet_name = name_by_calnet_uid(calnet_uid)
                task = change_password_task.delay(
                    account,
                    password,
                    comment=f'Your password was reset online by {calnet_name}.',
                )
                result = task.wait(timeout=5)
                if isinstance(result, Exception):
                    raise result
            except ValueError as ex:
                error = str(ex)
            else:
                # deleting this session variable will force the next
                # change_password request to reauthenticate with CalNet
                del request.session['calnet_uid']

                return render(
                    request,
                    'account/chpass/success.html',
                    {
                        'account': account,
                        'title': 'Password Changed Successfully',
                    },
                )
    else:
        form = ChpassForm(accounts, calnet_uid)

    return render(
        request,
        'account/chpass/index.html',
        {
            'calnet_uid': calnet_uid,
            'error': error,
            'form': form,
            'title': 'Reset Password',
        },
    )


class ChpassForm(Form):
    # fix self.fields.keyOrder type error in mypy
    field_order = [
        'ocf_account',
        'new_password',
        'confirm_password',
    ]

    def __init__(self, ocf_accounts: List[str], calnet_uid: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.calnet_uid = calnet_uid
        self.fields['ocf_account'] = forms.ChoiceField(
            choices=[(x, x) for x in ocf_accounts],
            label='OCF account',
        )

        # mypy expects fields to be a dict, but it isn't. This is defined in django so it can't be fixed
        # self.fields.keyOrder = field_order

    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label='New password',
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm password',
    )

    def clean_ocf_account(self) -> str:
        data = self.cleaned_data['ocf_account']
        if not user_exists(data):
            raise forms.ValidationError('OCF user account does not exist.')

        extra = ''

        ocf_accounts = get_accounts_for(self.calnet_uid)
        try:
            ocf_accounts += get_accounts_signatory_for(self.calnet_uid)
        except ConnectionError:
            extra = CALLINK_ERROR_MSG + '\n'

        if data not in ocf_accounts:
            raise forms.ValidationError(
                extra + 'OCF user account and CalNet UID mismatch.',
            )

        return data

    def clean_confirm_password(self) -> str:
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Your passwords don't match.")
        return confirm_password
