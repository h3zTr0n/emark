from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from messagestuff.models import Message
from django.contrib.auth.models import User
from accountstuff.models import UserInfo
from itertools import chain
from operator import attrgetter
import json

#UTILITY FUNCTIONS

def getMessages(howmany, page, kindof, targetusername, mark=True):
	target = User.objects.filter(username=targetusername)
	if (len(target) == 0):
		return {"error": "user does not exist"}
	messages = []
	if (kindof == "to"):
		messages = Message.objects.filter(recipient=target).order_by('timestamp')[(page*howmany):(page*howmany)+howmany]
	elif (kindof == "from"): #oldest first all over! not "-timestamp"
		messages = Message.objects.filter(sender=target).order_by('timestamp')[(page*howmany):(page*howmany)+howmany]
	if (mark):
		for mess in messages:
			if (mess.status == 1):
				mess.status = 2
				mess.save()
	return messages

def getMessagesSpecific(howmany, page, user1, user2, mark=True):
	user1 = User.objects.filter(username=user1)[0] #who you're talking to
	user2 = User.objects.filter(username=user2)[0] #you
	messages1 = Message.objects.filter(sender=user1, recipient=user2)
	messages2 = Message.objects.filter(sender=user2, recipient=user1)
	#result_list = list(chain(messages1, messages2))
	if (mark):
		for mess in messages1:
			if (mess.status == 1):
				mess.status = 2
				mess.save()
		# for mess in messages2:
		# 	if (mess.status == 1):
		# 		mess.status = 2
		# 		mess.save()
	allmessages = chain(messages1, messages2)
	#return sorted(allmessages,key=attrgetter('timestamp'))[(page*howmany):(page*howmany)+howmany]
	return sorted(allmessages,key=attrgetter('timestamp'))[(page*howmany):(page*howmany)+howmany]

def getUnreadMessages(touser, fromuser):
	messages = Message.objects.filter(sender=fromuser, recipient=touser)[0:100]
	count = 0
	for msg in messages:
		if (msg.status < 2):
			count += 1
	return count

#CLIENT VIEWS

def main(request, username):
	context = {}
	if (username != ""):
		context["requestedUser"] = User.objects.filter(username=username)[0]
	if (len(User.objects.filter(username=username))):
		context["requestedUserInfo"] = UserInfo.objects.filter(user=context["requestedUser"])
		context["specificmessages"] = getMessagesSpecific(100,0,username,request.user.username)
	recmes = getMessages(100,0,"to",request.user.username,False)
	#context["temptome"] = recmes
	seen = []
	context["msgusers"] = []
	for msgg in recmes:
		if (not msgg.sender in seen):
			context["msgusers"].append({
				"sender": msgg.sender,
				"unread": getUnreadMessages(request.user, msgg.sender)
			})
			seen.append(msgg.sender)
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	template = loader.get_template('Dmessages.html')
	return HttpResponse(template.render(RequestContext(request, context)))

'''
def mainWithUser(request, username):
	return HttpResponse("todo")
'''
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
	howmany = 10
	page = 0
	kindof = "to"
	target = request.user.username
	if "custom" in request.POST:
		howmany = request.POST["length"]
		page = request.POST["page"]
		kindof = request.POST["specification"] #"from" or "to"
		target = request.POST["target"]
	msgs = list(getMessages(howmany, page, kindof, target))
	for msg in msgs:
		msg['sender'] = msg['sender'].username;
		msg['recipient'] = msg['recipient'].username;
		msg['timestamp'] = msg['timestamp'].strftime("%B %d, %Y %I:%M:%S %p")
	return HttpResponse(json.dumps(msgs))

def unreadMessages(request):
	msgs = list(getMessages(100,0,"to",request.user.username,False))
	count = 0
	for msg in msgs:
		if (msg.status < 2):
			count += 1
	return HttpResponse(count)
'''
def viewMessagesOld(request):
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
'''
