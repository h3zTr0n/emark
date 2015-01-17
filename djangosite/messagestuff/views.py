from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from messagestuff.models import Message
from django.contrib.auth.models import User

# Create your views here.
#SERVER
def allInfo(request):
	context = {
		"user": request.user,
		"sentTen": Message.objects.filter(sender=request.user).order_by('-timestamp')[:10],
		"recvTen": Message.objects.filter(recipient=request.user).order_by('-timestamp')[:10],
	}
	template = loader.get_template('SmsgInfo.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def sendMessage(request):
	recipient = request.POST["recipient"]
	body = request.POST["body"]
	posRec = User.objects.filter(username=recipient)
	if (len(posRec) == 0):
		return HttpResponse("User '" + recipient + "' does not exist.")
	message = Message(sender=request.user,recipient=posRec[0],body=body)
	message.save()
	return HttpResponse("Success! Sent from '" + request.user.username + "' to '" + posRec[0].username + "'")

def viewMessages(request):
	#recent/numberofmessages/whichpage, all/specificuser
	return HttpResponse("TODO")
