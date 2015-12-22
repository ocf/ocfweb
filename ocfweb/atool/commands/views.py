from django.shortcuts import render
from paramiko import AuthenticationException
from paramiko import SSHClient

from ocfweb.atool.commands.forms import CommandForm
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
        'commands.html', {
            'form': form,
            'command': command_to_run,
            'output': output,
            'error': error,
        },
    )
