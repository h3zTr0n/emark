from django.shortcuts import render
from messagestuff.models import Message
from django.contrib.auth.models import User

# Create your views here.
#SERVER
def allInfo(request):
	#

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