from django import forms
from django.forms import widgets
from django.shortcuts import render
from paramiko import AuthenticationException
from paramiko import SSHClient

from ocfweb.atool.constants import CMDS_HOST
from ocfweb.atool.constants import CMDS_HOST_KEYS_FILENAME


def commands(request):
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
            ssh.load_host_keys(CMDS_HOST_KEYS_FILENAME)
            try:
                ssh.connect(CMDS_HOST, username=username,
                            password=password)
            except AuthenticationException:
                error = 'Authentication failed. Did you type the wrong ' + \
                    'username or password?'

            if not error:
                _, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_run)
                output = ssh_stdout.read()
                error = ssh_stderr.read()
    else:
        form = CommandForm()

    return render(
        request,
        'commands/index.html', {
            'form': form,
            'command': command_to_run,
            'output': output,
            'error': error,
        },
    )


class CommandForm(forms.Form):
    username = forms.CharField(label='OCF username',
                               min_length=3,
                               max_length=8)
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Password',
                               min_length=8,
                               max_length=64)

    COMMAND_CHOICES = (
        ('/opt/ocf/bin/paper',
         'paper quota -- how many pages you have remaining this semester'),
        ('/usr/bin/quota -svQ',
         'disk quota -- how much disk space you have used and how much you ' +
         'have left'),
        ('/opt/ocf/bin/makehttp',
         'makehttp -- set up the web space for your OCF account'),
        ('echo yes | /opt/ocf/bin/makemysql',
         'makemysql -- reset your MySQL database password, or create a new ' +
         'MySQL database (copy down the password somewhere secure)'),
    )

    command_to_run = forms.ChoiceField(choices=COMMAND_CHOICES,
                                       label='Command to run',
                                       widget=widgets.RadioSelect)
