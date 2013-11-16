from ocf.forms import LoginForm
from django.forms import Form
from ocf.utils import password_matches
from ocf.decorators import login_required, https_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

@https_required
def login(request):
    error = None

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if password_matches(username, password):
                request.session["ocf_user"] = username
                return redirect_back(request)
            else:
                error = "Authentication failed. Did you type the wrong username or password?"
    else:
        form = LoginForm()

    return render_to_response("login.html", {
        "form": form,
        "error": error
    }, context_instance=RequestContext(request))

@https_required
@login_required
def logout(request):
    if request.method == "POST":
        form = Form(request.POST)

        if form.is_valid():
            del request.session["ocf_user"]
            return redirect_back(request)
    else:
        form = Form()

    return render_to_response("logout.html", {
            "user": request.session["ocf_user"]
    }, context_instance=RequestContext(request))

def redirect_back(request):
    """Return the user to the page they were trying to access, or the commands
    page if we don't know what they were trying to access."""
    if "login_return_path" not in request.session:
        request.session["login_return_path"] = reverse("commands")

    return HttpResponseRedirect(request.session["login_return_path"])
