from django.http import HttpResponse
from pprint import saferepr

def index(request):
        returnStr = "Hello world\n"

        returnStr += "pB"
        returnStr += "\n\n"
        for thing in dir(request.session):
            try:
                    hey = getattr(request.session, thing)
            except:
                    hey = "Nope"
            returnStr += "%s - %s\n" % (thing, hey)
        return HttpResponse(returnStr)
