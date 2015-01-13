from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from accountstuff.models import UserInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date

# Create your views here.
def info(request):
	context = {}
	if (request.user.is_authenticated()):
		posInfos = UserInfo.objects.filter(user=request.user)
		context = {
			"user": request.user,
			"userinfo": posInfos[0] if posInfos else None
		}
	template = loader.get_template('info.html')
	return HttpResponse(template.render(RequestContext(request, context)))
def profile(request):
	context = {}
	if (request.user.is_authenticated()):
		posInfos = UserInfo.objects.filter(user=request.user)
		context = {
			"user": request.user,
			"userinfo": posInfos[0] if posInfos else None
		}
	template = loader.get_template('profile.html')
	return HttpResponse(template.render(RequestContext(request, context)))
def settings(request):
        template = loader.get_template('accountSettings.html')
        return HttpResponse(template.render(RequestContext(request)))
def signin(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponse("Signed in as " + user.username)
	else:
		return HttpResponse("Unable to sign in.")
def signout(request):
	logout(request)
	return HttpResponse("Success! Logged out.")
def register(request):
	username = request.POST['username']
	if len(User.objects.filter(username=username)) is not 0:
		return HttpResponse("Error: Username taken.")
	email = request.POST['email']
	password = request.POST['password']
	fname = request.POST['firstname']
	lname = request.POST['lastname']
	user = User.objects.create_user(username, email, password, first_name=fname, last_name=lname)
	
	bio = request.POST['bio']
	gender = request.POST['gender']
	birthday = date(int(request.POST['year']), int(request.POST['month']), int(request.POST['day']))
	phonenumber = request.POST['phonenumber']
	userinfo = UserInfo(user=username, bio=bio, gender=gender, birthday=birthday, phonenumber=phonenumber)
	
	user.save()
	userinfo.save()
	return HttpResponse("Success! Registered user " + username)