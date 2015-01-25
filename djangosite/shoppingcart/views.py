from django.shortcuts import render
from django.http import HttpResponse
from shoppingcart.models import ShoppingCartItem
from itemstuff.models import Item
from django.template import RequestContext, loader

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
	newItem = ShoppingCartItem(user = request.user, item = Item.objects.filter(itemid = itemid)[0], quantity = quantity)
	newItem.save()
	return HttpResponse("Success!!!!!!!!!")
def sumCartPrices(request, cartlist):
	sum = 0.0
	for cartitem in cartlist:
		sum += cartitem.item.price
	return sum