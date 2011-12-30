from django.http import HttpResponse
from pprint import saferepr

def index(request):
        returnStr = "Hello world\n"

        returnStr += "HIa10\n"

        returnStr += "\n\n"
        for thing in dir(request.user):
            try:
                    hey = getattr(request.user, thing)
            except:
                    hey = "Nope"
            returnStr += "%s - %s\n" % (thing, hey)
        return HttpResponse(returnStr)
