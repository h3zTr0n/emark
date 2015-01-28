from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from accountstuff.models import UserInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from itemstuff.models import Item
import random

#CLIENT
def getProfile(request, username):
	posUsers = User.objects.filter(username=username)
	context = {
		"requestedUser": None,
		"requestedUserInfo": None,
		"requestedUserFollowerInfos": None,
		"notFound": False,
		"self": False,
		"itemsList": None,
		"followed": False
	}
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	if (len(posUsers) > 0):
		context["requestedUser"] = posUsers[0]
		context["requestedUserInfo"] = UserInfo.objects.filter(user__username=username)[0]
		if(len(Item.objects.filter(user = context["requestedUser"])) > 0):
			context["itemsList"] = Item.objects.filter(user = context["requestedUser"])
		requestedUserFollowers = context["requestedUserInfo"].followers.all()
		requestedUserFollowerInfos = []
		for follower in requestedUserFollowers:
			if follower == request.user:
				context["followed"] = True
			requestedUserFollowerInfos.append(UserInfo.objects.filter(user=follower)[0])
		if(len(requestedUserFollowers) > 0):
			context["requestedUserFollowerInfos"] = requestedUserFollowerInfos
	if (len(posUsers) == 0):
		context["notFound"] = True
	if (request.user.username == username):
		context["self"] = True
	

	template = loader.get_template('Dprofile.html')
	return HttpResponse(template.render(RequestContext(request, context)))
def settings(request):
	if (not request.user.is_authenticated()):
		return HttpResponseRedirect("/acc/#signin")
	context = {
		"user": request.user,
		"userinfo": UserInfo.objects.filter(user=request.user)[0]
	}
	template = loader.get_template('Dsettings.html')
	return HttpResponse(template.render(RequestContext(request, context)))

'''
def signup(request): #gone
	template = loader.get_template('signup.html')
	return HttpResponse(template.render(RequestContext(request)))
'''

def main(request):
	if (request.user.is_authenticated()):
		return HttpResponseRedirect("/user/"+request.user.username+"/")
	template = loader.get_template('Dloginsignup.html')
	return HttpResponse(template.render(RequestContext(request)))

def signout(request):
	logout(request)
	return HttpResponseRedirect("/")

#SERVER
def info(request):
	context = {}
	if (request.user.is_authenticated()):
		posInfos = UserInfo.objects.filter(user=request.user)
		context = {
			"user": request.user,
			"userinfo": posInfos[0] if posInfos else None
		}
	template = loader.get_template('Sinfo.html')
	return HttpResponse(template.render(RequestContext(request, context)))
def signin(request):
	#username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	pos = User.objects.filter(email=email)
	if (len(pos) == 0):
		return HttpResponse("User does not exist.")
	else:
		pos = pos[0]
	user = authenticate(username=pos.username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponse("Signed in as " + user.username) #TODO redirect? nah brah
	else:
		return HttpResponse("Password wrong.")
def register(request):
	name = request.POST['name'].split(" ")
	fname = name.pop(0)
	lname = " ".join(name)
	'''
	if (not username in request.POST):
		username = request.POST['firstname'] + request.POST['lastname']
		username = username.replace(" ", "").lower() + random.randint(0,9) + "" + random.randint(0,9) + "" + random.randint(0,9) + "" + random.randint(0,9) + "" + random.randint(0,9)
	else:
		username = request.POST['username']
	if len(User.objects.filter(username=username)) is not 0:
		return HttpResponse("Error: Username taken.")
	'''
	username = request.POST["name"].replace(" ", "").lower() + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
	email = request.POST['email']
	password = request.POST['password']
	#fname = request.POST['firstname']
	#lname = request.POST['lastname']
	user = User.objects.create_user(username, email, password, first_name=fname, last_name=lname)
	
	gender = request.POST['gender']
	birthday = date(int(request.POST['year']), int(request.POST['month']), int(request.POST['day']))
	
	userinfo = UserInfo(user=user, gender=gender, birthday=birthday)
	
	user.save()
	userinfo.save()
	return HttpResponse("Success! Registered user " + username) #TODO redirect? 

def updateSettings(request):
	user=request.user
	userinfo = UserInfo.objects.filter(user=user)[0]

	if ('firstname' in request.POST and request.POST['firstname']):
		user.first_name = request.POST['firstname']
	if ('lastname' in request.POST and request.POST['lastname']):
		user.last_name = request.POST['lastname']
	if ('email' in request.POST and request.POST['email']):
		user.email = request.POST['email']
	if ('password' in request.POST and request.POST['password']):
		user.set_password(request.POST['password'])

	if ('bio' in request.POST and request.POST['bio']):
		userinfo.bio=request.POST['bio']
	if ('phonenumber' in request.POST and request.POST['phonenumber']):
		userinfo.phonenumber=request.POST['phonenumber']
	if ('pic' in request.FILES and request.FILES['pic']):
		userinfo.profile_picture = request.FILES['pic']

	if('oldpassword' in request.POST and request.POST['oldpassword']
		and 'password' in request.POST and request.POST['password']
		and 'passwordagain' in request.POST and request.POST['passwordagain']):
		oldpassword = request.POST['oldpassword']
		password = request.POST['password']
		newpassword = request.POST['passwordagain']
		if(oldpassword == user.password and password == newpassword):
			user.password = newpassword

	user.save()
	userinfo.save()
	return HttpResponse("Success! Settings were changed") #TODO redirect?

def follow(request, username):
	masterInfo = UserInfo.objects.filter(user = User.objects.filter(username = username)[0])[0]
	slaveInfo = UserInfo.objects.filter(user = request.user)[0]
	if slaveInfo != masterInfo:
		slaveInfo.following.add(masterInfo.user)
		masterInfo.followers.add(slaveInfo.user)
		slaveInfo.save()
		masterInfo.save()
	return HttpResponseRedirect("/user/" + username + "/")
def unfollow(request, username):
	masterInfo = UserInfo.objects.filter(user = User.objects.filter(username = username)[0])[0]
	slaveInfo = UserInfo.objects.filter(user = request.user)[0]
	if slaveInfo != masterInfo:
		slaveInfo.following.remove(masterInfo.user)
		masterInfo.followers.remove(slaveInfo.user)
	return HttpResponseRedirect("/user/" + username +"/")