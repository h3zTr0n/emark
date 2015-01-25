from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from shoppingcart.models import ShoppingCartItem
from itemstuff.models import Item
from django.template import RequestContext, loader
import random

# Create your views here.
def displayCart(request):
	shoppingCart = ShoppingCartItem.objects.filter(user = request.user)
	context = {
		"CartList" : shoppingCart,
		"user" : request.user,
		"cartListSum": sumCartPrices(request, shoppingCart)
	}
	template = loader.get_template('DshoppingCart.html')
	return HttpResponse(template.render(RequestContext(request, context)))
def addItemToUser(request, itemid, quantity):
	if len(ShoppingCartItem.objects.filter(user = request.user, item = Item.objects.filter(itemid = itemid)[0])) == 0:
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
