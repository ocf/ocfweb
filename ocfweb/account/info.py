from django import forms
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from ocflib.printing.quota import get_connection
from ocflib.printing.quota import get_quota
from ocflib.vhost.application import get_app_vhosts
from ocflib.vhost.mail import vhosts_for_user
from ocflib.vhost.web import get_vhosts
from paramiko import AuthenticationException
from paramiko import SSHClient
from paramiko.hostkeys import HostKeyEntry

from ocfweb.auth import login_required
from ocfweb.component.forms import Form
from ocfweb.component.session import logged_in_user


@login_required
def account_info(request: HttpRequest) -> HttpResponse:
    user = logged_in_user(request)
    with get_connection() as c:
        paper_quota = get_quota(c, user)
    bytes_used = None
    bytes_total = None
    error = ''
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            ssh = SSHClient()
            host_keys = ssh.get_host_keys()
            entry_ed25519 = HostKeyEntry.from_line(
                'ssh.ocf.berkeley.edu ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPm+RlDujsxQyxFTEOCTeImSBDvr63cL8Kg+rNrH6NK8',  # noqa
            )
            entry_rsa = HostKeyEntry.from_line(
                'ssh.ocf.berkeley.edu ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAqMkHVVoMl8md25iky7e2Xe3ARaC4H1PbIpv5Y+xT4KOT17gGvFSmfjGyW9P8ZTyqxq560iWdyELIn7efaGPbkUo9retcnT6WLmuh9nRIYwb6w7BGEEvlblBmH27Fkgt7JQ6+1sr5teuABfIMg22WTQAeDQe1jg0XsPu36OjbC7HjA3BXsiNBpxKDolYIXWzOD+r9FxZLP0lawh8dl//O5FW4ha1IbHklq2i9Mgl79wAH3jxf66kQJTvLmalKnQ0Dbp2+vYGGhIjVFXlGSzKsHAVhuVD6TBXZbxWOYoXanS7CC43MrEtBYYnc6zMn/k/rH0V+WeRhuzTnr/OZGJbBBw==',  # noqa
            )
            host_keys.add(
                'ssh.ocf.berkeley.edu',
                'ssh-ed25519',
                entry_ed25519.key,
            )
            host_keys.add(
                'ssh.ocf.berkeley.edu',
                'ssh-rsa',
                entry_rsa.key,
            )

            try:
                ssh.connect(
                    'ssh.ocf.berkeley.edu',
                    username=user,
                    password=password,
                )
            except AuthenticationException:
                error = 'Authentication failed. Did you type the wrong password?'

            if not error:
                quota_command = "/run/current-system/sw/bin/quota 2>/dev/null | awk 'NR==3 {print $2, $3}'"
                _, ssh_stdout, _ = ssh.exec_command(quota_command, get_pty=True)
                sizes = ssh_stdout.read().decode().split()
                if len(sizes) == 2:
                    bytes_used, bytes_total = (int(size) * 1024 for size in sizes)
                else:
                    error = 'Unable to get quota information from the server. Please try again later.'
    else:
        form = PasswordForm()

    return render(
        request,
        'account/info/index.html', {
            'title': 'My Account',
            'form': form,
            'error': error,
            'paper_quota': paper_quota,
            'bytes_used': bytes_used,
            'bytes_total': bytes_total,
            'vhosts': [
                {'host': host, 'aliases': val['aliases']}
                for host, val in get_vhosts().items()
                if val['username'] == user
            ],
            'vhosts_app': [
                {'host': host, 'aliases': val['aliases']}
                for host, val in get_app_vhosts().items()
                if val['username'] == user
            ],
            'vhosts_mail': vhosts_for_user(user),
        },
    )


class PasswordForm(Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='',
        min_length=8,
        max_length=256,
    )
