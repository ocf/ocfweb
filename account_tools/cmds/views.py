from django.shortcuts import render_to_response
from django.template import RequestContext
from ocf.decorators import https_required

@https_required
def commands(request):
    if request.method == "POST":
        pass
    else:
        pass
    form = "hi"
    return render_to_response("commands.html", {
        "form": form,
    }, context_instance=RequestContext(request))
