from cmds.forms import CommandForm
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from ocf.decorators import https_required
from paramiko import AuthenticationException, SSHClient

@https_required
def commands(request):
    command_to_run = ''
    output = ''
    error = ''
    if request.method == "POST":
        form = CommandForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            command_to_run = form.cleaned_data['command_to_run']

            ssh = SSHClient()
            ssh.load_host_keys(settings.CMDS_HOST_KEYS_FILENAME)
            try:
                ssh.connect(settings.CMDS_HOST, username=username, password=password)
            except AuthenticationException, ae:
                error = "Authentication failed. Did you type the wrong username or password?"
                
            if not error:
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_run)
                output = ssh_stdout.read()
                error = ssh_stderr.read()
    else:
        form = CommandForm()

    return render_to_response("commands.html", {
        "form": form,
        "command": command_to_run,
        "output": output,
        "error": error,
    }, context_instance=RequestContext(request))
