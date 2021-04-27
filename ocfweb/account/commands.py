from django import forms
from django.forms import widgets
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from paramiko import AuthenticationException
from paramiko import SSHClient
from paramiko.hostkeys import HostKeyEntry

from ocfweb.component.forms import Form


def commands(request: HttpRequest) -> HttpResponse:
    command_to_run = ''
    output = ''
    error = ''
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            command_to_run = form.cleaned_data['command_to_run']

            ssh = SSHClient()

            host_keys = ssh.get_host_keys()
            entry = HostKeyEntry.from_line(
                'ssh.ocf.berkeley.edu ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAqMkHVVoMl8md25iky7e2Xe3ARaC4H1PbIpv5Y+xT4KOT17gGvFSmfjGyW9P8ZTyqxq560iWdyELIn7efaGPbkUo9retcnT6WLmuh9nRIYwb6w7BGEEvlblBmH27Fkgt7JQ6+1sr5teuABfIMg22WTQAeDQe1jg0XsPu36OjbC7HjA3BXsiNBpxKDolYIXWzOD+r9FxZLP0lawh8dl//O5FW4ha1IbHklq2i9Mgl79wAH3jxf66kQJTvLmalKnQ0Dbp2+vYGGhIjVFXlGSzKsHAVhuVD6TBXZbxWOYoXanS7CC43MrEtBYYnc6zMn/k/rH0V+WeRhuzTnr/OZGJbBBw==',  # noqa
            )
            assert entry is not None  # should never be none as we are passing a static string above
            host_keys.add(
                'ssh.ocf.berkeley.edu',
                'ssh-rsa',
                entry.key,
            )

            try:
                ssh.connect(
                    'ssh.ocf.berkeley.edu',
                    username=username,
                    password=password,
                )
            except AuthenticationException:
                error = 'Authentication failed. Did you type the wrong username or password?'

            if not error:
                _, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_run, get_pty=True)
                output = ssh_stdout.read().decode()
                error = ssh_stderr.read().decode()
    else:
        form = CommandForm()

    return render(
        request,
        'account/commands/index.html', {
            'title': 'Account commands',
            'form': form,
            'command': command_to_run,
            'output': output,
            'error': error,
        },
    )


class CommandForm(Form):
    username = forms.CharField(
        label='OCF username',
        min_length=3,
        max_length=16,
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password',
        min_length=8,
        max_length=256,
    )

    COMMAND_CHOICES = (
        (
            '/opt/share/utils/bin/paper',
            'paper quota -- how many pages you have remaining this semester',
        ),
        (
            '/usr/bin/quota -svQ',
            'disk quota -- how much disk space you have used and how much you ' +
            'have left',
        ),
        (
            '/opt/share/utils/bin/makehttp',
            'makehttp -- set up the web space for your OCF account',
        ),
        (
            'echo yes | /opt/share/utils/bin/makemysql',
            'makemysql -- reset your MySQL database password, or create a new ' +
            'MySQL database (copy down the password somewhere secure)',
        ),
    )

    command_to_run = forms.ChoiceField(
        choices=COMMAND_CHOICES,
        label='Command to run',
        widget=widgets.RadioSelect,
    )
