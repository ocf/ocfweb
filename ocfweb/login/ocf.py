import re
from typing import Any
from typing import Match
from typing import Optional
from typing import Union

import ocflib.account.search as search
import ocflib.account.utils as utils
import ocflib.account.validators as validators
from django import forms
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from ocflib.account.search import user_is_sorried

from ocfweb.auth import login_required
from ocfweb.component.forms import Form
from ocfweb.component.session import logged_in_user
from ocfweb.component.session import login as session_login
from ocfweb.component.session import logout as session_logout


def _valid_return_path(return_to: str) -> Optional[Match[Any]]:
    """Make sure this is a valid relative path to prevent redirect attacks."""
    return re.match(
        '^/[^/]',
        return_to,
    )


def login(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponse]:
    error = None

    return_to = request.GET.get('next')
    if return_to and _valid_return_path(return_to):
        request.session['login_return_path'] = return_to

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                if (
                        search.user_exists(username) and not
                        user_is_sorried(username) and
                        utils.password_matches(username, password)
                ):
                    session_login(request, username)
                    return redirect_back(request)
                else:
                    error = (
                        'Authentication failed. Your account may be disabled, '
                        'or you may have typed the wrong username or password.'
                    )
            except ValueError as ex:
                error = 'Authentication failed: {error}'.format(
                    error=str(ex),
                )
    else:
        form = LoginForm()

    return render(
        request,
        'login/ocf/login.html',
        {
            'title': 'OCF Login',
            'form': form,
            'error': error,
        },
    )


@login_required
def logout(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponse]:
    return_to = request.GET.get('next')
    if return_to and _valid_return_path(return_to):
        request.session['login_return_path'] = return_to

    if request.method == 'POST':
        form = forms.Form(request.POST)

        if form.is_valid():
            session_logout(request)
            return redirect_back(request)
    else:
        form = forms.Form()

    return render(
        request,
        'login/ocf/logout.html',
        {
            'form': form,
            'user': logged_in_user(request),
        },
    )


def redirect_back(request: HttpRequest) -> HttpResponseRedirect:
    """Return the user to the page they were trying to access, or the home
    page if we don't know what they were trying to access.
    """
    return HttpResponseRedirect(
        request.session.pop('login_return_path', reverse('home')),
    )


class LoginForm(Form):
    username = forms.CharField(
        label='OCF username',
        min_length=3,
        max_length=16,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password',
        min_length=8,
        max_length=64,
    )

    def clean_username(self) -> str:
        username = self.cleaned_data.get('username', '')
        return username.strip().lower()
