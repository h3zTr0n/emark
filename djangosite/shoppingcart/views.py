from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from shoppingcart.models import ShoppingCartItem
from itemstuff.models import Item
from django.template import RequestContext, loader
from accountstuff.models import Address, CreditCards, UserInfo
import random

# Create your views here.
def displayCart(request):
	shoppingCart = ShoppingCartItem.objects.filter(user = request.user, pending = False, received = False)
	context = {
		"CartList" : shoppingCart,
		"user" : request.user,
		"cartListSum": sumCartPrices(request, shoppingCart),
		"numItems" : len(shoppingCart),
		"pendingItems" : ShoppingCartItem.objects.filter(user=  request.user, pending = True, received = False),
		"receivedItems" : ShoppingCartItem.objects.filter(user = request.user, received = True),
		"pendingOrders" : getPendingOrders(request),
		"finishedOrders" : getFinishedOrders(request),
	}
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	template = loader.get_template('DshoppingCart.html')
	return HttpResponse(template.render(RequestContext(request, context)))
def addItemToUser(request, itemid, quantity):
	if len(ShoppingCartItem.objects.filter(user = request.user, item = Item.objects.filter(itemid = itemid)[0], pending = False)) == 0:
		newItem = ShoppingCartItem(user = request.user, item = Item.objects.filter(itemid = itemid)[0], quantity = quantity, uniqueid = "sci" + Item.objects.filter(itemid = itemid)[0].title.replace(" ", "").lower() +  str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
	else :
		newItem = ShoppingCartItem.objects.filter(user = request.user, item = Item.objects.filter(itemid = itemid)[0])[0]
		newItem.quantity += int(quantity)
	newItem.save()
	return HttpResponseRedirect("/cart/")
def sumCartPrices(request, cartlist):
	sum = 0.0
	for cartitem in cartlist:
		sum += cartitem.item.price * cartitem.quantity
	return sum
def removeItem(request, scitemid):
	removedItem = ShoppingCartItem.objects.filter(uniqueid = scitemid)
	removedItem.delete()
	#return displayCart(request)
	return HttpResponseRedirect("/cart/")
def shipping(request):
	if len(Address.objects.filter(user = request.user)) > 0:
		return HttpResponseRedirect("/cart/checkout/pPayment/")
	return HttpResponseRedirect("/cart/checkout/#shipping")
def payment(request):
	if len(CreditCards.objects.filter(user=request.user)) > 0:
		return HttpResponseRedirect("/cart/checkout/pSubmitOrder/")
	newAddress = Address(user = request.user, country = request.POST['country'], street = request.POST['street'], aptsuiteother = request.POST['aptsuiteother'], zipcode = request.POST['zipcode'], city = request.POST['city'], state = request.POST['state'])
	newAddress.save()
	
	return HttpResponseRedirect("/cart/checkout/#payment")
def submitOrder(request):
	if len(CreditCards.objects.filter(user=request.user)) > 0:
		return HttpResponseRedirect("/cart/checkout/#submitorder")
	creditCard = CreditCards(user = request.user, cardNumber = request.POST['cardNumber'], monthExp = request.POST['ExpMonth'], yearExp = request.POST['ExpYear'], securityCode = request.POST['securityCode'])
	creditCard.save()
	return HttpResponseRedirect("/cart/checkout/#submitorder")
def checkout(request):
	context = {
		"user" : request.user,
		"address" : None,
		"creditcard": None,
		"cartlist": ShoppingCartItem.objects.filter(user = request.user, pending = False),
	}
	if (request.user.is_authenticated()):
		context["user"] = request.user
		context["userinfo"] = UserInfo.objects.filter(user=request.user)[0]
	if len(Address.objects.filter(user = request.user)) > 0:
		context['address'] = Address.objects.filter(user = request.user)[0]
	if len(CreditCards.objects.filter(user=request.user)) > 0:
		context['creditcard'] = CreditCards.objects.filter(user=request.user)[0]
	template = loader.get_template('Dcheckout.html')
	return HttpResponse(template.render(RequestContext(request, context)))

def clearOrder(request):
	itemList = ShoppingCartItem.objects.filter(user = request.user)
	for k in range(0, len(itemList)):
		itemList[k].pending = True
		itemList[k].save()
	return HttpResponseRedirect("/cart/")

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
	return HttpResponseRedirect("/cart/")
def removeItem(request, cartitemid):
	item = ShoppingCartItem.objects.filter(uniqueid = cartitemid, received = True)
	item.delete()
	return HttpResponseRedirect("/cart/")