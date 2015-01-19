from django.shortcuts import render
from django.http import HttpResponse
from shoppingcart.models import ShoppingCartItem
from itemstuff.models import Item

# Create your views here.
def displayCart(request):
	shoppingCart = ShoppingCartItem.objects.filter(user = request.user)
	return HttpResponse(shoppingCart)
def addItemToUser(request, itemid, quantity):
	newItem = ShoppingCartItem(user = request.user, item = Item.objects.filter(itemid = itemid)[0], quantity = quantity)
	newItem.save()
	return HttpResponse("Success!!!!!!!!!")