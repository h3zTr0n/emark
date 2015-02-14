from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from accountstuff.models import UserInfo, Address, CreditCards
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from itemstuff.models import Item
from shoppingcart.models import ShoppingCartItem

import random

#CLIENT
def isEmailTaken(request):
	if (len(User.objects.filter(email=request.GET["email"])) > 0):
		return HttpResponse(User.objects.filter(email=request.GET["email"])[0].username)
	else:
		return HttpResponse("AVAILABLE")
def getProfile(request, username):
	posUsers = User.objects.filter(username=username)
	context = {
		"requestedUser": None,
		"requestedUserInfo": None,
		"requestedUserFollowerInfos": None,
		"self": False,
		"itemsList": None,
		"followed": False
	}
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
	if (request.user.username == username):
		context["self"] = True
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]

	template = loader.get_template('Dprofile.html')
	return HttpResponse(template.render(RequestContext(request, context)))
def settings(request):
	if (not request.user.is_authenticated()):
		return HttpResponseRedirect("/acc/#signin")
	context = {
		"user": request.user,
		"userinfo": UserInfo.objects.filter(user=request.user)[0],
	}
	if len(Address.objects.filter(user = request.user)) > 0:
		context["address"] = Address.objects.filter(user = request.user)[0]
	if len(CreditCards.objects.filter(user = request.user)) > 0:
		context["ccinfo"] = CreditCards.objects.filter(user = request.user)[0]
	template = loader.get_template('Dsettings.html')
	return HttpResponse(template.render(RequestContext(request, context)))

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
		return HttpResponse("Error: User does not exist.")
	else:
		pos = pos[0]
	user = authenticate(username=pos.username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponse("Signed in as " + user.username) #TODO redirect? nah brah
	else:
		return HttpResponse("Error: Password wrong.")
def register(request):
	if not ("name" in request.POST and "email" in request.POST and "password" in request.POST and request.POST['name'] and request.POST['email'] and request.POST['password']):
		return HttpResponse("Error: Missing Fields.")
	name = request.POST['name'].split(" ")
	fname = name.pop(0)
	lname = " ".join(name)
	
	username = request.POST["name"].replace(" ", "").lower() + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
	email = request.POST['email']
	password = request.POST['password']
	#fname = request.POST['firstname']
	#lname = request.POST['lastname']
	if len(User.objects.filter(email=email)) is not 0:
		return HttpResponse("Error: Email taken.")
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

	user.save()
	userinfo.save()
	return HttpResponseRedirect("/user/" + user.username + "/")

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

def updateAddress(request):
	currentAddress = Address.objects.filter(user = request.user)[0]
	currentAddress.country = request.POST['country']
	currentAddress.street = request.POST['street']
	currentAddress.aptsuiteother = request.POST['aptsuiteother']
	currentAddress.zipcode = request.POST['zipcode']
	currentAddress.city = request.POST['city']
	currentAddress.state = request.POST['state']
	currentAddress.save()
	return HttpResponseRedirect("/acc/settings/")

def updateCC(request):
	currentCC = CreditCards.objects.filter(user = request.user)[0]
	if currentCC == None:
		currentCC= CreditCards(user = request.user, cardNumber = request.POST['cardNumber'], monthExp = request.POST['ExpMonth'], yearExp = request.POST['ExpYear'] , securityCode =request.POST['securityCode'] )
	else:
		currentCC.cardNumber = request.POST['cardNumber']
		currentCC.monthExp = request.POST['ExpMonth']
		currentCC.yearExp = request.POST['ExpYear']
		currentCC.securityCode = request.POST['securityCode']
	currentCC.save()
	return HttpResponseRedirect("/acc/settings/")

def getPendingOrders(request):
	yourItemList = Item.objects.filter(user = request.user)
	pendingOrders = []
	for item in yourItemList:
		pendingOrders += ShoppingCartItem.objects.filter(item = item, pending = True, received = False)
	return pendingOrders

def getFinishedOrders(request):
	yourItemList = Item.objects.filter(user = request.user)
	finishedOrders = []
	for item in yourItemList:
		finishedOrders += ShoppingCartItem.objects.filter(item = item, received = True)
	return finishedOrders
def receivedItem(request, cartitemid) :
	item = ShoppingCartItem.objects.filter(uniqueid = cartitemid, received = False)[0]
	item.received = True
	item.save()
	return HttpResponseRedirect("/acc/purchaseHistory/#pending")
def removeFinishedItem(request, cartitemid):
	item = ShoppingCartItem.objects.filter(uniqueid = cartitemid, received = True)
	item.delete()
	return HttpResponseRedirect("/cart/")

def purchaseHistory(request):
	context ={
		"user" : None,
		"userinfo" : None,
		"finishedOrders":None,
		"pendingItems":None,
		"pendingOrders": None,
		"receivedItems":None,
	}
	if request.user.is_authenticated():
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
		context["finishedOrders"] = getFinishedOrders(request)
		context["receivedItems"] = ShoppingCartItem.objects.filter(user = request.user, received = True)
		context["pendingOrders"] = getPendingOrders(request)
		context["pendingItems"] = ShoppingCartItem.objects.filter(user = request.user, pending = True, received = False)
		context["pendingOrdersLength"] = len(context["pendingOrders"])
		context["finishedOrdersLength"]= len(context["finishedOrders"])
		context["pendingItemsLength"] =len(context["pendingItems"])
		context["receivedItemsLength"] = len(context["receivedItems"])
	template=loader.get_template('purchaseHistory.html')
	return HttpResponse(template.render(RequestContext(request, context)))
