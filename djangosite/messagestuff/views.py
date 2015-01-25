from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from messagestuff.models import Message
from django.contrib.auth.models import User
import json

# Create your views here.
#client
def main(request):
	return HttpResponse("todo")

def mainWithUser(request, username):
	return HttpResponse("todo")

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
	howmany = 10
	page = 0
	kindof = "to"
	target = request.user.username
	if "custom" in request.POST:
		howmany = request.POST["length"]
		page = request.POST["page"]
		kindof = request.POST["specification"] #"from" or "to"
		target = request.POST["target"]

	target = User.objects.filter(username=target)
	if (len(target) == 0):
		return HttpResponse("User does not exist.")

	messages = None
	if (kindof == "to"):
		messages = Message.objects.filter(recipient=target).order_by('timestamp')[(page*howmany):(page*howmany)+howmany]
	elif (kindof == "from"): #oldest first all over! not "-timestamp"
		messages = Message.objects.filter(sender=target).order_by('timestamp')[(page*howmany):(page*howmany)+howmany]
	
	msgobj = []
	for msg in messages:
		msgobj.append({
			"sender": msg.sender.username,
			"recipient": msg.recipient.username,
			"timestamp": msg.timestamp.strftime("%B %d, %Y %I:%M:%S %p"),
			"body": msg.body,
		})

	return HttpResponse(json.dumps(msgobj))
