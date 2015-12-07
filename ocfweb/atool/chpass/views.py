from django.shortcuts import render_to_response
from django.template import RequestContext

from ocfweb.atool.calnet.decorators import login_required as calnet_required
from ocfweb.atool.chpass.forms import ChpassForm
from ocfweb.atool.chpass.forms import get_authorized_accounts_for
from ocfweb.atool.ocf.tasks import change_password as change_password_task


@calnet_required
def change_password(request):
    calnet_uid = request.session['calnet_uid']
    accounts = get_authorized_accounts_for(calnet_uid)
    error = None

    if request.method == 'POST':
        form = ChpassForm(accounts, calnet_uid, request.POST)
        if form.is_valid():
            account = form.cleaned_data['ocf_account']
            password = form.cleaned_data['new_password']

            try:
                task = change_password_task.delay(account, password)
                result = task.wait(timeout=5)
                if isinstance(result, Exception):
                    raise result
            except ValueError as ex:
                error = str(ex)
            else:
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
            'error': error,
        },
        context_instance=RequestContext(request)
    )
