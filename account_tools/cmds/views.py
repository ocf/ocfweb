from cmds.forms import CommandForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from ocf.decorators import https_required
from paramiko import SSHClient

@https_required
def commands(request):
    if request.method == "POST":
        asdf
    else:
        pass
    form = CommandForm()
    return render_to_response("commands.html", {
        "form": form,
    }, context_instance=RequestContext(request))
