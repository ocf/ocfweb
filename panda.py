#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from chpass.forms import ChpassForm
from ocf.utils import users_by_calnet_uid
from calnet.decorators import login_required as calnet_required

@calnet_required
def index(request):
    if not "ocf_accounts" in request.session:
        request.session["ocf_accounts"] = users_by_calnet_uid(request.session["calnet_uid"])
    accounts = request.session["ocf_accounts"]

    dump = {}

    if request.method == "POST":
        form = ChpassForm(accounts, request.POST)
        if form.is_valid():
            dump["form"] = "VALID"
    else:
        form = ChpassForm(accounts)
    return render_to_response("test.html", {
        "form": form,
        "dump": dump
    }, context_instance=RequestContext(request))
