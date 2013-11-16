from ocf.utils import user_attrs, user_is_group
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from vhost.forms import VirtualHostForm
from ocf.decorators import https_required, login_required, group_account_required
from django.core.urlresolvers import reverse
from paramiko import AuthenticationException, SSHClient

@login_required
@group_account_required
def request_vhost(request):
    user_account = request.session["ocf_user"]
    attrs = user_attrs(user_account)

    if request.method == "POST":
        form = VirtualHostForm(request.POST)
    else:
        form = VirtualHostForm(initial={"requested_subdomain": user_account})

    group_url = "http://www.ocf.berkeley.edu/~{0}/".format(user_account)

    return render_to_response("request_vhost.html", {
        "form": form,
        "user": user_account,
        "attrs": attrs,
        "group_url": group_url
    }, context_instance=RequestContext(request))

    """
    if request.method == "POST":
        form = CommandForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

    else:
        form = CommandForm()
   
    return render_to_response("request_vhost.html", {
        "form": form,
        "command": command_to_run,
        "output": output,
        "error": error,
    })
    """
