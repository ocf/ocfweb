import ocflib.account.utils as utils
import ocflib.account.validators as validators
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ocfweb.auth import login_required


def login(request):
    error = None

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                if (validators.user_exists(username) and
                        utils.password_matches(username, password)):
                    request.session['ocf_user'] = username
                    return redirect_back(request)
                else:
                    error = 'Authentication failed. Did you type the wrong ' + \
                        'username or password?'
            except ValueError as ex:
                error = 'Authentication failed: {error}'.format(
                    error=str(ex),
                )
    else:
        form = LoginForm()

    return render(
        request,
        'ocf/login.html',
        {
            'form': form,
            'error': error,
        },
    )


@login_required
def logout(request):
    if request.method == 'POST':
        form = forms.Form(request.POST)

        if form.is_valid():
            del request.session['ocf_user']
            return redirect_back(request)
    else:
        form = forms.Form()

    return render(
        request,
        'ocf/logout.html',
        {
            'form': form,
            'user': request.session['ocf_user']
        },
    )


def redirect_back(request):
    """Return the user to the page they were trying to access, or the commands
    page if we don't know what they were trying to access."""
    if 'login_return_path' not in request.session:
        request.session['login_return_path'] = reverse('commands')

    return HttpResponseRedirect(request.session['login_return_path'])


class LoginForm(forms.Form):
    username = forms.CharField(label='OCF username',
                               min_length=3,
                               max_length=8)
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Password',
                               min_length=8,
                               max_length=64)

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        return username.strip().lower()
