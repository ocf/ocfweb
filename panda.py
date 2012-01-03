#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from recaptcha.fields import ReCaptchaField

class TestForm(forms.Form):
    name = forms.CharField()
    recaptcha = ReCaptchaField()

def index(request):
	dump = {}
        if request.method == "POST":
            form = TestForm(request.POST)
            if form.is_valid():
                dump["form"] = "VALID"
        else:
            form = TestForm()
            
        return render_to_response("test.html", {
        	"form": form,
        	"dump": dump
        }, context_instance=RequestContext(request))
