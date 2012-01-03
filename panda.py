from django.http import HttpResponse
from calnet.decorators import login_required

@login_required
def index(request):
        returnStr = "Hello world\n"
        
        returnStr += "calnet_uid in session: "
        if "calnet_uid" in request.session:
        	returnStr += "True"
        else:
        	returnStr += "False"
        	
        returnStr += "\n\n"
     	returnStr += "Calnet UID: "
     	if "calnet_uid" in request.session:
     		returnStr += str(request.session["calnet_uid"])
     	else:
     		returnStr += "Nothing"
     	returnStr += "\n\n"
     	
     	returnStr = returnStr.replace("\n", "<br />\n")
        return HttpResponse(returnStr)
