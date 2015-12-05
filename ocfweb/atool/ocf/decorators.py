import ocflib.account.search as search
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


def login_required(function):
    def _decorator(request, *args, **kwargs):
        if 'ocf_user' in request.session:
            return function(request, *args, **kwargs)

        request.session['login_return_path'] = request.get_full_path()
        return HttpResponseRedirect(reverse('login'))

    return _decorator


def group_account_required(function):
    def _decorator(request, *args, **kwargs):
        if search.user_is_group(request.session['ocf_user']):
            return function(request, *args, **kwargs)

        return render(request, 'group_accounts_only.html', {
            'user': request.session['ocf_user']
        }, status=403)

    return _decorator
