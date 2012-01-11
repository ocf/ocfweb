#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from chpass.forms import ChpassForm

def index(request):
	dump = {}
        if request.method == "POST":
            form = ChpassForm(request.POST)
            if form.is_valid():
                dump["form"] = "VALID"
        else:
            form = ChpassForm()
            
        return render_to_response("test.html", {
        	"form": form,
        	"dump": dump
        }, context_instance=RequestContext(request))
